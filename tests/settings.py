"""
Django settings for testing django_pgwatch
"""

import os

SECRET_KEY = 'test-secret-key-not-for-production'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_pgwatch',
]

USE_TZ = True

# Required for ArrayField in testing
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
DATABASES['default']['NAME'] = os.environ.get('POSTGRES_DB', 'test_pgwatch')
DATABASES['default']['USER'] = os.environ.get('POSTGRES_USER', 'postgres')
DATABASES['default']['PASSWORD'] = os.environ.get('POSTGRES_PASSWORD', 'postgres')
DATABASES['default']['HOST'] = os.environ.get('POSTGRES_HOST', 'localhost')
DATABASES['default']['PORT'] = os.environ.get('POSTGRES_PORT', '5432')
