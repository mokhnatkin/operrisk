"""
Django settings for operrisk_project project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

def read_key(fn):#function is used to read *.key files    
    key = None
    try:
        with open('keys/'+fn+'.key','r') as f:
            key = f.readline().strip()
    except:
        raise IOError(fn+'.key file not found')
    return key


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')
MEDIA_DIR = os.path.join(BASE_DIR,'media')

STATICFILES_DIRS = [STATIC_DIR, ]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = read_key('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ngrok.io','localhost','127.0.0.1','a62fb173.ngrok.io',]


# Application definition

INSTALLED_APPS = [
    'registration',#django-registration-redux package
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'operrisk',
    'bootstrap3',
    'django_filters',
    'django_python3_ldap',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'operrisk_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'operrisk_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

"""sqLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
#mySQL
DB_USER = read_key('DB_USER')
DB_PASSWORD = read_key('DB_PASSWORD')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'operrisk_db',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_L10N = False#changed to False to apply DATE_FORMAT (see below)
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

# setting for SelectDateWidget (add incident form, incident_date)
DATE_FORMAT = 'j N, Y'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'

#settings for django-registration-redux app
REGISTRATION_OPEN = False
LOGIN_REDIRECT_URL = '/operrisk/'
LOGIN_URL = '/accounts/login/'

#settings for django-python3-ldap
AUTHENTICATION_BACKENDS = ('django_python3_ldap.auth.LDAPBackend',)
LDAP_AUTH_URL = read_key('LDAP_AUTH_URL')#88.204.147.90
LDAP_AUTH_SEARCH_BASE = "dc=amanat,dc=local"
LDAP_AUTH_CONNECTION_USERNAME = read_key('LDAP_AUTH_CONNECTION_USERNAME')
LDAP_AUTH_CONNECTION_PASSWORD = read_key('LDAP_AUTH_CONNECTION_PASSWORD')
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "amanat"

LDAP_AUTH_USER_FIELDS = {
    "username": "sAMAccountName",#sAMAccountName
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

LDAP_AUTH_OBJECT_CLASS = "user"

#settings for EXCHANGE server - see module emailing.py
EXCHANGE_USERNAME = read_key('EXCHANGE_USERNAME')
EXCHANGE_PASSWORD = read_key('EXCHANGE_PASSWORD')
PRIMARY_SMTP_ADDRESS = read_key('PRIMARY_SMTP_ADDRESS')