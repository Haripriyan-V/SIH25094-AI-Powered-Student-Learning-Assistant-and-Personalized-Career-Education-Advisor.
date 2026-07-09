from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'interests', views.InterestViewSet, basename='interest')
router.register(r'skills', views.SkillViewSet, basename='skill')
router.register(r'profiles', views.StudentProfileViewSet, basename='student-profile')
router.register(r'education', views.EducationViewSet, basename='education')
router.register(r'my-skills', views.StudentSkillViewSet, basename='student-skill')

urlpatterns = [
    path('profile/me/', views.MyProfileView.as_view(), name='my-profile'),
    path('', include(router.urls)),
]
