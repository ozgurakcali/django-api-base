import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'o*(zh4b8*9hzi#9=4(ep##0s9!#e$%@ee5ghj3qwrdb73v^f_='

DEBUG = True

AUTH_USER_MODEL = 'profiles.User'


# Security
CSRF_TRUSTED_ORIGINS = [
    '127.0.0.1:4200',
    'localhost:4200',
    '127.0.0.1:8080',
    'localhost:8080',
]

CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:4200',
    'localhost:4200',
    '127.0.0.1:8080',
    'localhost:8080',
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'user-agent',
    'accept-encoding',
    'x-authtoken'
)

CORS_EXPOSE_HEADERS = [
    'x-authtoken'
]

ALLOWED_HOSTS = [
    '*'
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'common',
    'profiles',
    'authentication',
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

ROOT_URLCONF = 'django_api_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'django_api_base.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('dbname'),
        'USER': os.environ.get('dbuser'),
        'PASSWORD': os.environ.get('dbpass'),
        'HOST': os.environ.get('dbhost'),
        'PORT': os.environ.get('dbport')
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Authentication
JWT_SECRET = "@@YbAf.+N#yHi^RU"


# Date formats
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_TIME_FORMAT = '%H:%M:%S'
DEFAULT_DATE_TIME_FORMAT = DEFAULT_DATE_FORMAT + ' ' + DEFAULT_TIME_FORMAT

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'common.paginators.NormalizedLimitOffsetPagination',

    'EXCEPTION_HANDLER': 'common.exceptions.base_exception_handler',

    'DEFAULT_RENDERER_CLASSES': (
        'common.renderers.NormalizedJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.authenticators.JwtTokenAuthentication'
    ]
}
