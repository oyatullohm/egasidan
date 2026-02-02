import os
from pathlib import Path
from datetime import timedelta
import environ

# --------------------------------------------------
# BASE
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
SECRET_KEY = env.str('SECRET_KEY')

# firebase_credentials_json = env.str("FIREBASE_CREDENTIALS")
# FIREBASE_CREDENTIALS = json.loads(firebase_credentials_json)
FIREBASE_CREDENTIALS = os.path.join(BASE_DIR, "Admin/firebase-key.json")

FIREBASE_SERVER_KEY = env.str('FIREBASE_SERVER_KEY')
FIREBASE_CONFIG = {
    'apiKey': env.str('FIREBASE_API_KEY'),
    'authDomain': env.str('FIREBASE_AUTH_DOMAIN'),
    'projectId': env.str('FIREBASE_PROJECT_ID'),
    'storageBucket': env.str('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': env.str('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': env.str('FIREBASE_APP_ID'),
}

FIREBASE_VAPID_KEY = env.str('FIREBASE_VAPID_KEY')
DEBUG = True
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'announcement',
    'drf_spectacular',
    'rest_framework',
    'rest_framework_simplejwt',

]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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




REST_USE_JWT = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        
    ),
    'DEFAULT_PARSER_CLASSES': [
    'rest_framework.parsers.JSONParser',
    'rest_framework.parsers.MultiPartParser',  # <- BU QATORNI QO'SHING
    'rest_framework.parsers.FormParser',
],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Elonchi API',
    'VERSION': '1.0.0',
    # O'rnatilgan avtomatik aniqlash uchun JWT authentication klassini ko'rsating:
    'AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    # Tokenni har so'rovda qayta kiritmaslik uchun:
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Admin.urls'
WSGI_APPLICATION = 'Admin.wsgi.application'


from .set_database import *
DATABASES = LOCAL_DATABASE


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGGING = {
    'version':1,
    'handlers':{
         'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log'
        },
        'console':{'class':'logging.StreamHandler'}
    },
    'loggers':{
        'django.db.backends':{
            'handlers':['file'],
            'level':'DEBUG'
                    }
               }
}  


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# STATIC / MEDIA
# --------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --------------------------------------------------
# DEFAULT
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'main.CustomUser'
# Firebase init (IMPORTANT)
import Admin.firebase
