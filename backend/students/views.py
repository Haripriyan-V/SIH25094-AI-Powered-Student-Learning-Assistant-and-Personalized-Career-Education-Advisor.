from rest_framework import viewsets, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import IsOwnerOrAdmin, IsCounselorOrAdmin
from .models import StudentProfile, StudentSkill, Education, Interest, Skill
from .serializers import (
    StudentProfileSerializer, StudentSkillSerializer,
    EducationSerializer, InterestSerializer, SkillSerializer,
)


class InterestViewSet(viewsets.ModelViewSet):
    """Catalog of interests. Read access for all authenticated users; write for counselors/admins."""
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SkillViewSet(viewsets.ModelViewSet):
    """Catalog of skills. Read access for all authenticated users; write for counselors/admins."""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'category']
    filterset_fields = ['category']


class MyProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/students/profile/me/
    Fetch or update the logged-in student's profile. Auto-creates the
    profile on first access so the frontend never has to special-case 404.
    """
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile


class StudentProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only listing of student profiles, intended for counselors/admins
    browsing students (e.g. for career guidance).
    """
    queryset = StudentProfile.objects.select_related('user').prefetch_related('interests', 'skills')
    serializer_class = StudentProfileSerializer
    permission_classes = [IsCounselorOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email', 'school_or_college']


class EducationViewSet(viewsets.ModelViewSet):
    """CRUD for the logged-in student's own education history."""
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return Education.objects.filter(student_profile=profile)

    def perform_create(self, serializer):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student_profile=profile)


class StudentSkillViewSet(viewsets.ModelViewSet):
    """CRUD for the logged-in student's own skills."""
    serializer_class = StudentSkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return StudentSkill.objects.filter(student_profile=profile)

    def perform_create(self, serializer):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(student_profile=profile)
