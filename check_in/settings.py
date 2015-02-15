"""
Django settings for testy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUTH_USER_MODEL = 'registration.RegisteredUser'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nuuj*6xly9i@eia==^fyi4k3xn%0gcc-$s&vhahyv**6sb%t#g'

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
    'debug_toolbar',
    'django_extensions',
    'django_forms_bootstrap',
    'djcelery',

    'registration',
    #'network.providers.hp',
    'network.providers.hp.procurve_2650',
    #'network.providers.hp.procurve_2524',
    'network.providers.hp.procurve_2626',
    #'network.providers.cisco',
    'network.providers.cisco.catalyst_2950',
    'network.providers.mikrotik',

    'network',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'check_in.middleware.RemoteAddrMiddleware',
)

ROOT_URLCONF = 'check_in.urls'

WSGI_APPLICATION = 'check_in.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/s/'
STATIC_ROOT = os.path.join(BASE_DIR, "_static")

TEMPLATE_URL = '/t/'
#TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR, "_templates"),
#)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "_static"),
#)

#print os.path.join(BASE_DIR, "_static")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
            },
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },

    }
}


BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TASK_SERIALIZER = "json"

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

VERIFICATION_OVERRIDE_CODE = 'BCGamer12'

DIRTY_SUBNETS = '10.0.2'