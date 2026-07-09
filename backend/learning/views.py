from django.utils import timezone
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import IsCounselorOrAdmin
from .models import (
    Subject, Course, LearningResource, Quiz, Question, Choice,
    QuizAttempt, StudentProgress, Scholarship, College,
)
from .serializers import (
    SubjectSerializer, CourseSerializer, CourseListSerializer,
    LearningResourceSerializer, QuizSerializer, QuizPublicSerializer,
    QuestionSerializer, ChoiceSerializer, QuizAttemptSerializer,
    QuizSubmissionSerializer, StudentProgressSerializer,
    ScholarshipSerializer, CollegeSerializer,
)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CourseViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for courses.
    - List/Retrieve: any user (AllowAny) — matches Career recommendation pattern.
    - Create/Update/Delete: counselors/admins only.
    """
    queryset = Course.objects.select_related('subject', 'created_by').prefetch_related('resources').filter(is_published=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'level']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'duration_hours', 'title']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsCounselorOrAdmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, pk=None):
        """POST /api/learning/courses/{id}/enroll/ -> start tracking progress for this student."""
        course = self.get_object()
        progress, created = StudentProgress.objects.get_or_create(
            student=request.user, course=course,
            defaults={'status': StudentProgress.Status.IN_PROGRESS, 'progress_percent': 0},
        )
        serializer = StudentProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class LearningResourceViewSet(viewsets.ModelViewSet):
    """
    - List/Retrieve: AllowAny — students can browse resources.
    - Create/Update/Delete: counselors/admins only.
    """
    queryset = LearningResource.objects.select_related('course')
    serializer_class = LearningResourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'resource_type']
    search_fields = ['title']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsCounselorOrAdmin()]
        return [AllowAny()]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related('course').prefetch_related('questions__choices')
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list') and not (
            self.request.user.is_authenticated and (
                self.request.user.is_staff or
                getattr(self.request.user, 'role', None) in ('counselor', 'admin')
            )
        ):
            return QuizPublicSerializer
        return QuizSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request, pk=None):
        """
        POST /api/learning/quizzes/{id}/submit/
        Body: {"answers": {"<question_id>": <choice_id>, ...}}
        Grades the quiz and records a QuizAttempt for the logged-in student.
        """
        quiz = self.get_object()
        serializer = QuizSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = serializer.validated_data['answers']

        questions = quiz.questions.prefetch_related('choices')
        total = questions.count()
        correct = 0

        for question in questions:
            chosen_choice_id = answers.get(str(question.id)) or answers.get(question.id)
            if chosen_choice_id is None:
                continue
            is_correct = Choice.objects.filter(
                id=chosen_choice_id, question=question, is_correct=True
            ).exists()
            if is_correct:
                correct += 1

        score = round((correct / total) * 100, 2) if total else 0
        passed = score >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            student=request.user, quiz=quiz, score=score, passed=passed,
            completed_at=timezone.now(),
        )
        return Response(
            {
                'attempt': QuizAttemptSerializer(attempt).data,
                'correct_answers': correct,
                'total_questions': total,
            },
            status=status.HTTP_201_CREATED,
        )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('quiz').prefetch_related('choices')
    serializer_class = QuestionSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quiz']


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.select_related('question')
    serializer_class = ChoiceSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question']


class QuizAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    """Students see only their own attempts; counselors/admins see all."""
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quiz', 'passed']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'role', None) in ('counselor', 'admin'):
            return QuizAttempt.objects.select_related('quiz', 'student').all()
        return QuizAttempt.objects.select_related('quiz').filter(student=user)


class StudentProgressViewSet(viewsets.ModelViewSet):
    """Tracks each student's progress through courses. Students manage only their own records."""
    serializer_class = StudentProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'role', None) in ('counselor', 'admin'):
            return StudentProgress.objects.select_related('course', 'student').all()
        return StudentProgress.objects.select_related('course').filter(student=user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


# ---------------------------------------------------------------------------
# Scholarship ViewSet
# ---------------------------------------------------------------------------

class ScholarshipViewSet(viewsets.ModelViewSet):
    """
    Scholarship catalog.
    - List/Retrieve: AllowAny — students can browse without login.
    - Create/Update/Delete: counselors/admins only.
    """
    queryset = Scholarship.objects.filter(is_active=True)
    serializer_class = ScholarshipSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['scholarship_type']
    search_fields = ['name', 'provider', 'eligibility']
    ordering_fields = ['name', 'amount', 'deadline', 'created_at']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsCounselorOrAdmin()]
        return [AllowAny()]


# ---------------------------------------------------------------------------
# College ViewSet
# ---------------------------------------------------------------------------

class CollegeViewSet(viewsets.ModelViewSet):
    """
    College / university catalog.
    - List/Retrieve: AllowAny — students can browse without login.
    - Create/Update/Delete: counselors/admins only.
    """
    queryset = College.objects.filter(is_active=True)
    serializer_class = CollegeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['college_type']
    search_fields = ['name', 'location', 'affiliation']
    ordering_fields = ['ranking', 'name', 'established_year']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsCounselorOrAdmin()]
        return [AllowAny()]
