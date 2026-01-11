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


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    # Django default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',

    # Local apps
    'main',
    'announcement',

    # Third-party
    # 'corsheaders',
    'rest_framework',
    # 'rest_framework.authtoken',
    'rest_framework_simplejwt',

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',

    # 'dj_rest_auth',
    # 'dj_rest_auth.registration',
]

# SITE_ID = 1

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



# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# )


# --------------------------------------------------
# ALLAUTH SETTINGS (MUHIM QISM)
# --------------------------------------------------

# ACCOUNT_LOGIN_METHODS = {'email'}

# ACCOUNT_SIGNUP_FIELDS = {
#     "email": {"required": True},
#     "password1": {"required": True},
#     "password2": {"required": True},
# }

# ACCOUNT_EMAIL_VERIFICATION = "optional"


# --------------------------------------------------
# DJ-REST-AUTH
# --------------------------------------------------
REST_USE_JWT = True

# DJ_REST_AUTH = {
#     'USE_JWT': True,
#     'JWT_AUTH_HTTPONLY': False,
#     'SESSION_LOGIN': False,
#     'TOKEN_MODEL': None,
#     # Agar custom register serializer bo‘lsa:
#     # 'REGISTER_SERIALIZER': 'main.serializers.CustomRegisterSerializer',
# }


# --------------------------------------------------
# REST FRAMEWORK
# --------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
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
    # 'allauth.account.middleware.AccountMiddleware',
]

# CORS_ALLOW_ALL_ORIGINS = True


# --------------------------------------------------
# URL / WSGI
# --------------------------------------------------
ROOT_URLCONF = 'Admin.urls'
WSGI_APPLICATION = 'Admin.wsgi.application'


# --------------------------------------------------
# DATABASE
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         },
#         'APP': [
#             # Web application
#             {
#                 'client_id': '1087350409427-gns002aj7otkv8lqlp0r85k3p1i0luue.apps.googleusercontent.com' ,
#                 'secret': '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',
#                 'key': ''
#             },
     
#             {
#                 'client_id': 'ANDROID_CLIENT_ID.apps.googleusercontent.com',
#                 'secret': '', 
#                 'key': ''
#             },

#             {
#                 'client_id': 'IOS_CLIENT_ID.apps.googleusercontent.com',
#                 'secret': '',     
#                 'key': ''
#             }
#         ]
#     }
# }

SPECTACULAR_SETTINGS = {
    'TITLE': 'Egasidan API',
    'DESCRIPTION': 'API Hujjatlari',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [{'TokenAuth': []}],
    'COMPONENTS': {
        'securitySchemes': {
            'TokenAuth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
            }
        }
    }
}
# --------------------------------------------------
# PASSWORD VALIDATORS
# --------------------------------------------------
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
