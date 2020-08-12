"""
Django settings for championshipchallenge project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import dj_database_url
import os
import django_heroku

# ######################################################################################## #
# SETTINGS FOR BASE DIRECTORY
# ######################################################################################## #

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ######################################################################################## #
# SETTINGS FOR DEVELOPMENT AND PRODUCTION
# ######################################################################################## #

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('CHAMPIONSHIP_CHALLENGE_SECRET_KEY')

# local DEVELOPMENT_MODE env var is set to True, Heroku env var is set to False
DEVELOPMENT_MODE = (os.environ.get('DEVELOPMENT_MODE') == 'True')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEVELOPMENT_MODE


if DEVELOPMENT_MODE:
  ALLOWED_HOSTS = []
else:
  ALLOWED_HOSTS = ['championship-challenge.herokuapp.com']


# ######################################################################################## #
# SETTINGS FOR INSTALLED APPLICATIONS
# ######################################################################################## #

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'gameplay.apps.GameplayConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    # 3rd party
    'allauth',
    'allauth.account',
    'crispy_forms',
    'phonenumber_field',
    'stripe',
    'storages',
]


# ######################################################################################## #
# SETTINGS FOR MIDDLEWARE
# ######################################################################################## #

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'championshipchallenge.urls'

# ensure http redirects to https automatically
if not DEVELOPMENT_MODE:
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  SECURE_SSL_REDIRECT = True

# ######################################################################################## #
# SETTINGS FOR TEMPLATES
# ######################################################################################## #

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

WSGI_APPLICATION = 'championshipchallenge.wsgi.application'


# ######################################################################################## #
# SETTINGS FOR LOCAL DATABASE
# ######################################################################################## #

# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('CHAMPIONSHIP_CHALLENGE_DATABASE_NAME'),
        'USER': os.environ.get('CHAMPIONSHIP_CHALLENGE_DATABASE_USER'),
        'PASSWORD': os.environ.get('CHAMPIONSHIP_CHALLENGE_DATABASE_PASSWORD'),
        'HOST': os.environ.get('CHAMPIONSHIP_CHALLENGE_DATABASE_HOST'),
        'PORT': os.environ.get('CHAMPIONSHIP_CHALLENGE_DATABASE_PORT'),
    }
}


# ######################################################################################## #
# SETTINGS FOR PRODUCTION DATABASE (AWS postgresql)
# ######################################################################################## #

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# ######################################################################################## #
# SETTINGS FOR PASSWORD VALIDATION
# ######################################################################################## #

# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# ######################################################################################## #
# SETTINGS FOR INTERNATIONALIZATION
# ######################################################################################## #

# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ######################################################################################## #
# SETTINGS FOR STATIC FILES
# ######################################################################################## #

# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# needed for Heroku (staticfiles folder will be created)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')


# ######################################################################################## #
# SETTINGS FOR CRISPY FORMS
# ######################################################################################## #

# Tell crispy forms which style to use
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# ######################################################################################## #
# SETTINGS FOR LOGGING IN REDIRECTS
# ######################################################################################## #

# By default django wants to direct users to 'accounts/profile.html'
# after logging in - this overrides it
LOGIN_REDIRECT_URL = 'gameplay_home'
# By default if a view has the @login_required decorater, django tries
# to redirect to 'accounts/login' which doesn't exist
LOGIN_URL = 'account_login'


# ######################################################################################## #
# SETTINGS FOR DJANGO-ALLAUTH
# ######################################################################################## #

# allauth is required to provide custom registration details

ACCOUNT_LOGOUT_REDIRECT_URL = 'gameplay_home'
ACCOUNT_LOGOUT_ON_GET = True

AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}


# ######################################################################################## #
# SETTINGS FOR SENDING EMAILS
# ######################################################################################## #

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER_GMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS_GMAIL')


# ######################################################################################## #
# SETTINGS FOR STRIPE
# ######################################################################################## #

STRIPE_PRODUCT_SINGLE_ENTRY_PRICE_ID = os.environ.get(
    'STRIPE_PRODUCT_SINGLE_ENTRY_PRICE_ID')

if DEVELOPMENT_MODE:
  # test keys
  STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY_TEST')
  STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY_TEST')
else:
  # IMPORTANT! - if the payment is actually going live, switch to live keys below
  STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY_TEST')
  STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY_TEST')
  # STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY_LIVE')
  # STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY_LIVE')


# ######################################################################################## #
# SETTINGS FOR AMAZON AWS S3
# ######################################################################################## #

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

if not DEVELOPMENT_MODE:
  # look to s3 buckets for all static files including js and css
  STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# ######################################################################################## #
# SETTINGS FOR HEROKU CONNECTION
# ######################################################################################## #

# Activate Django-Heroku (staticfiles set to false to make sure heroku looks to s3)
django_heroku.settings(locals(), staticfiles=False)
