"""
Django settings for lingyun project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p2%@7((94u6epn$=^&=#*@xyyf*_xy+gpdl5(=(k9y385qh3#^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qsq',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lingyun.urls'

WSGI_APPLICATION = 'lingyun.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   # 'default': {
   #     'ENGINE': 'django.db.backends.sqlite3',
   #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hadoop',
        'USER':'hadoop',
        'PASSWORD':'123',
        'HOST':'localhost',
        'PORT':'',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

DEFAULT_CHARSET='utf-8'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS =(
    # Put strings here, like "/home/html/django_templates"or "C:/www/django/templates".
    "/root/workspace/lingyun/qsq/Templates",
    "/root/workspace/lingyun/qsq/Templates/display",
    # Always use forward slashes, even onWindows.
    # Don't forget to use absolute paths,not relative paths.
)

STATICFILES_DIRS= (
    os.path.join(BASE_DIR, "static"),
    '/root/workspace/lingyun/qsq/static',
    '/root/workspace/lingyun/qsq/static/upload',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
    'standard': {
                     'format': '%(levelname)s %(asctime)s %(message)s'
                },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'system_handler': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'/tmp/qsq_system.log',
            'formatter':'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'system':{
            'handlers': ['system_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
