from collections import defaultdict
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import IsCounselorOrAdmin
from .models import (
    CareerField, CareerPath, AssessmentTest, AssessmentQuestion,
    AssessmentOption, AssessmentResult, CareerRecommendation,
)
from .serializers import (
    CareerFieldSerializer, CareerPathSerializer, CareerPathListSerializer,
    AssessmentTestSerializer, AssessmentTestPublicSerializer,
    AssessmentQuestionSerializer, AssessmentOptionSerializer,
    AssessmentSubmissionSerializer, AssessmentResultSerializer,
    CareerRecommendationSerializer,
)


class CareerFieldViewSet(viewsets.ModelViewSet):
    queryset = CareerField.objects.all()
    serializer_class = CareerFieldSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CareerPathViewSet(viewsets.ModelViewSet):
    queryset = CareerPath.objects.select_related('career_field').prefetch_related('required_skills', 'related_interests')
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['career_field', 'growth_outlook']
    search_fields = ['title', 'description']
    ordering_fields = ['average_salary_lpa', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return CareerPathListSerializer
        return CareerPathSerializer


class AssessmentTestViewSet(viewsets.ModelViewSet):
    queryset = AssessmentTest.objects.filter(is_active=True).prefetch_related('questions__options')
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsCounselorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'role', None) in ('counselor', 'admin'):
            return AssessmentTestSerializer
        return AssessmentTestPublicSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request, pk=None):
        """
        POST /api/career/tests/{id}/submit/
        Body: {"answers": {"<question_id>": <option_id>, ...}}
        Scores answers by aggregating `score_weight` per related career field,
        then auto-generates top-3 CareerRecommendations from CareerPaths in
        the highest-scoring fields. (Rule-based baseline -- can be swapped
        for the ML/AI recommendation engine in a later phase.)
        """
        test = self.get_object()
        serializer = AssessmentSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = serializer.validated_data['answers']

        field_scores = defaultdict(int)
        questions = test.questions.prefetch_related('options')

        for question in questions:
            chosen_option_id = answers.get(str(question.id)) or answers.get(question.id)
            if chosen_option_id is None or not question.related_career_field_id:
                continue
            option = question.options.filter(id=chosen_option_id).first()
            if option:
                field_scores[str(question.related_career_field_id)] += option.score_weight

        result = AssessmentResult.objects.create(
            student=request.user, test=test, field_scores=dict(field_scores),
        )

        recommendations = self._generate_recommendations(request.user, result, field_scores)

        return Response(
            {
                'result': AssessmentResultSerializer(result).data,
                'recommendations': CareerRecommendationSerializer(recommendations, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def _generate_recommendations(student, result, field_scores, top_n=3):
        if not field_scores:
            return []

        max_score = max(field_scores.values()) or 1
        top_field_ids = sorted(field_scores, key=field_scores.get, reverse=True)[:top_n]

        recommendations = []
        for field_id in top_field_ids:
            normalized_score = round((field_scores[field_id] / max_score) * 100, 2)
            career_path = CareerPath.objects.filter(career_field_id=field_id).first()
            if not career_path:
                continue
            rec, _ = CareerRecommendation.objects.update_or_create(
                student=student, career_path=career_path, source_assessment=result,
                defaults={
                    'match_score': normalized_score,
                    'reasoning': (
                        f"Based on your assessment answers, you showed strong affinity "
                        f"towards the '{career_path.career_field.name}' field, making "
                        f"'{career_path.title}' a strong fit."
                    ),
                },
            )
            recommendations.append(rec)
        return recommendations


class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    queryset = AssessmentQuestion.objects.select_related('test', 'related_career_field').prefetch_related('options')
    serializer_class = AssessmentQuestionSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['test']


class AssessmentOptionViewSet(viewsets.ModelViewSet):
    queryset = AssessmentOption.objects.select_related('question')
    serializer_class = AssessmentOptionSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question']


class AssessmentResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssessmentResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['test']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'role', None) in ('counselor', 'admin'):
            return AssessmentResult.objects.select_related('test', 'student').all()
        return AssessmentResult.objects.select_related('test').filter(student=user)

class CareerRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CareerRecommendationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['career_path']
    ordering_fields = ['match_score', 'generated_at']

    def get_queryset(self):
        return CareerRecommendation.objects.select_related(
            'career_path__career_field',
            'student'
        ).all()


class MyRecommendationsView(APIView):
    """GET /api/career/my-recommendations/ -> shortcut for the logged-in student's latest recommendations."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        recs = CareerRecommendation.objects.select_related('career_path__career_field').filter(
            student=request.user
        ).order_by('-match_score')[:10]
        return Response(CareerRecommendationSerializer(recs, many=True).data)
