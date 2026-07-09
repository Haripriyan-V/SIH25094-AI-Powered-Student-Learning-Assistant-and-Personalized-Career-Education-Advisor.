"""
Django settings for SIH25094 - AI-Powered Student Learning Assistant
and Personalized Career & Education Advisor.
"""
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------
# SECURITY
# --------------------------------------------------------------------
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-please-change')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

# --------------------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',

    # Local apps
    'accounts',
    'students',
    'learning',
    'career',
    'chatbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# --------------------------------------------------------------------
# DATABASE (MySQL)
# --------------------------------------------------------------------
DB_ENGINE = config('DB_ENGINE', default='sqlite')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME', default='sih25094_db'),
            'USER': config('DB_USER', default='root'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='127.0.0.1'),
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    # SQLite fallback for local development when MySQL is not configured.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --------------------------------------------------------------------
# CUSTOM USER MODEL
# --------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'

# --------------------------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------
# STATIC & MEDIA FILES
# --------------------------------------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# --------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
}

# --------------------------------------------------------------------
# SIMPLE JWT
# --------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('ACCESS_TOKEN_LIFETIME_MIN', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('REFRESH_TOKEN_LIFETIME_DAYS', default=7, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# --------------------------------------------------------------------
# CORS
# --------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

CORS_ALLOW_CREDENTIALS = True
