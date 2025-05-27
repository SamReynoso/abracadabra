import os
from dotenv import load_dotenv

from pathlib import Path


load_dotenv()


WSGI_APPLICATION = 'project.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

ALLOWED_HOSTS = []
SECRET_KEY =  os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ROOT_URLCONF = 'project.urls'
STATIC_URL = 'static/'
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 2
LOGIN_REDIRCT_URL = '/user/profile/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/user/profile/'

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

    'app',
    'core',
    'user',
    'info',
    'marketing',
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
        'NAME': BASE_DIR / '../db.sqlite3',
    }
}

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': V_P + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': V_P + 'MinimumLengthValidator',
    },
    {
        'NAME': V_P + 'CommonPasswordValidator',
    },
    {
        'NAME': V_P + 'NumericPasswordValidator',
    },
]

