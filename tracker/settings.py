"""
Django settings for tracker project.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open( os.path.abspath( 'tracker/secret_key.txt' ) ) as f:
    SECRET_KEY = f.read().strip()

DEBUG = True

ALLOWED_HOSTS = ['.ctrack.xyz']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'lists',
    'password_reset', # github.com/brutasse/django-password-reset
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.abspath( 'tracker/templates' ),
            os.path.abspath( 'accounts/templates' ),
            os.path.abspath( 'lists/templates' ),
        ],
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

WSGI_APPLICATION = 'tracker.wsgi.application'


# Email, used for password recovery

with open( os.path.abspath( 'tracker/email.txt' ) ) as f:
    emdata = f.read().strip().split('+')

    EMAIL_HOST = emdata[0]
    EMAIL_PORT = emdata[1]
    EMAIL_HOST_PASSWORD = emdata[2]
    EMAIL_HOST_USER = emdata[3]
    SERVER_EMAIL = emdata[4]
    ADMINS = (('Chris', emdata[4]),)
    EMAIL_SUBJECT_PREFIX = ''
    EMAIL_USE_TLS = True


# Database

with open( os.path.abspath( 'tracker/db.txt' ) ) as f:
    dbdata = f.read().strip().split('+')
    
    DATABASES = {
        'default': {
            'ENGINE': dbdata[0],
            'NAME': dbdata[1],
            'USER': dbdata[2],
            'PASSWORD': dbdata[3],
            'HOST': dbdata[4],
            'PORT': dbdata[5],
        }
    }

# Login url, used by @login_required
LOGIN_URL = '/accounts/login/'

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join( os.path.join( os.path.dirname(BASE_DIR), 'public' ), 'static' )
STATICFILES_DIRS = [
    os.path.abspath( 'tracker/static' ),
]