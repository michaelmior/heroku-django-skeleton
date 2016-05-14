# Django settings for project.
import os

DEBUG = True if os.environ.get('DJANGO_DEBUG', None) == '1' else False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.herokuapp.com').split(':')
SITE_DOMAIN = ALLOWED_HOSTS[0]
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

import dj_database_url
DATABASES = {'default': dj_database_url.config()}

from redisify import redisify
CACHES = redisify(default='redis://localhost/0')

# Configure sessions using Redis. This depends on the caching settings above.
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST, SESSION_REDIS_PORT = \
        CACHES['default']['LOCATION'].split(':')
SESSION_REDIS_PORT = int(SESSION_REDIS_PORT)
SESSION_REDIS_DB = CACHES['default']['OPTIONS']['DB']
SESSION_REDIS_PASSWORD = CACHES['default']['OPTIONS']['PASSWORD']
SESSION_REDIS_PREFIX = 'sess'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Use Redis as the broker for Celery tasks
BROKER_URL = (lambda password, db: 'redis://:%%s@%(LOCATION)s/%%d' \
        % CACHES['default'] % (password, db))( \
          CACHES['default']['OPTIONS']['PASSWORD'] or '',
          CACHES['default']['OPTIONS']['DB'] or 0,
        )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# While debugging, use the built-in server's static file serving mechanism.
# In production, host all files on S3.
if os.environ.get('AWS_ACCESS_KEY_ID'):
    # Access information for the S3 bucket
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME

    # Static files are stored in the bucket at /static
    # and user-uploaded files are stored at /media
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = 'media'
    STATIC_S3_PATH = 'static'
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False

    # Construct the paths to resources on S3 via
    # the bucket name and the necessary paths
    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    MEDIA_URL = '//%s.s3.amazonaws.com/%s/' % \
            (AWS_STORAGE_BUCKET_NAME, DEFAULT_S3_PATH)
    STATIC_ROOT = '/%s/' % STATIC_S3_PATH
    STATIC_URL = '//%s.s3.amazonaws.com/%s/' % \
            (AWS_STORAGE_BUCKET_NAME, STATIC_S3_PATH)
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
else:
    STATIC_ROOT = 'static'
    STATIC_URL = '/static/'
    MEDIA_ROOT = 'media'
    MEDIA_URL = '/media/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

TEMPLATES = [
    {
        'DEBUG': DEBUG,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'app.main.context_processors.settings',
            'app.main.context_processors.site',

            'django.core.context_processors.request',
            'django.contrib.auth.context_processors.auth'
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        }
    }
]

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'app.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'app.wsgi.application'

INSTALLED_APPS = (
    'app.main',
    'app.bootstrap',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'gunicorn',
    'djcelery',
    'djangosecure',
)

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60 * 60  # 1 hour
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
