from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'fields', views.CareerFieldViewSet, basename='career-field')
router.register(r'paths', views.CareerPathViewSet, basename='career-path')
router.register(r'tests', views.AssessmentTestViewSet, basename='assessment-test')
router.register(r'questions', views.AssessmentQuestionViewSet, basename='assessment-question')
router.register(r'options', views.AssessmentOptionViewSet, basename='assessment-option')
router.register(r'results', views.AssessmentResultViewSet, basename='assessment-result')
router.register(r'recommendations', views.CareerRecommendationViewSet, basename='career-recommendation')

urlpatterns = [
    path('my-recommendations/', views.MyRecommendationsView.as_view(), name='my-recommendations'),
    path('', include(router.urls)),
]
