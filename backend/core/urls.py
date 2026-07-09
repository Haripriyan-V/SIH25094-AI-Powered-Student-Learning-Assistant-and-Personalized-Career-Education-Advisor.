from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT token endpoints
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App-level APIs
    path('api/accounts/', include('accounts.urls')),
    path('api/students/', include('students.urls')),
    path('api/learning/', include('learning.urls')),
    path('api/career/', include('career.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
