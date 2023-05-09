from pathlib import Path
import os
from django.conf import settings
from dotenv import load_dotenv
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

load_dotenv(verbose=True)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = []
if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.getenv('ALLOWED_HOSTS').split(','))

DEVELOPMENT = False
# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.gis',#django gis activation
    #developer added libraries
    # 'debug_toolbar',
    'django.contrib.sitemaps',
    'ckeditor',
    'hitcount',
    'captcha',
    'django.contrib.sites',
    #user apps
    'users',
    'services',
    'payments',
    'geemap',
    ]
SITE_ID = 1
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pnb_main.urls'

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
                'django.template.context_processors.i18n',

            ],
        },
    },
]
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#         'LOCATION': '127.0.0.1:8000',
#     }
# }

WSGI_APPLICATION = 'pnb_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
gettext = lambda s: s
LANGUAGES = (
    ('en', _('English')),
    ('ro', _('Română')),
    ('de', _('Deutsch')),
)

#==============EMAIL SETTINGS==========================
#-----test
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
#-----production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#-----email credentials
EMAIL_PORT=os.getenv('EMAIL_PORT')
EMAIL_HOST=os.getenv('EMAIL_HOST')
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER='contact@bucegipark.ro'
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }
# ============ django-resized settings ====================
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_SCALE = 0.5
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'WebP'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'WebP': ".WebP"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

#================django simple captcha======================
CAPTCHA_IMAGE_SIZE = (100,50)
CAPTCHA_BACKGROUND_COLOR = "#2eb872"
CAPTCHA_FOREGROUND_COLOR = "black"
#===================Default primary key field type
#================https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
