import os
from dotenv import load_dotenv

from pathlib import Path


load_dotenv()


WSGI_APPLICATION = 'project.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "abracadabrasports.com",
        "www.abracadabrasports.com"
        ]

CSRF_TRUSTED_ORIGINS = [
        "https://www.abracadabrasports.com",
        "https://abracadabrasports.com"
        ]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True


SECRET_KEY =  os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
SITE_ID = int(os.getenv("DJANGO_SITE_ID", "1"))

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = 'project.urls'
STATIC_URL = 'static/'
STATIC_ROOT = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.parent / 'www' / 'media'

ACCOUNT_SIGNUP_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False


SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "email"

SOCIALACCOUNT_LOGIN_ON_GET=True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.auth',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'models',
    'core',

    'persona',
    'app',
    'discover',
    'search',
#    'gameday',
#    'info',
#    'marketing',
]


MIDDLEWARE = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'allauth.account.middleware.AccountMiddleware',

]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'www' / 'db.sqlite3',
        }
    }

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'abs_db',
#        'USER': os.getenv("DB_USER", "abs_admin"),
#        'PASSWORD': os.getenv("DB_PASSWORD", "password"),
#        'HOST': os.getenv("DB_HOST", "localhost"),
#        'PORT': os.getenv("DB_PORT", ""),
#    }
#}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

V_P = 'django.contrib.auth.password_validation.'

AUTH_USER_MODEL = 'models.User'
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': V_P + 'UserAttributeSimilarityValidator', },
    { 'NAME': V_P + 'MinimumLengthValidator', },
    { 'NAME': V_P + 'CommonPasswordValidator', },
    { 'NAME': V_P + 'NumericPasswordValidator', },
]

