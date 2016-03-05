import os


def local_path(path):
    os.path.join(os.path.dirname(__file__), path)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': ':memory:'
    }
}

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'survey',
    'tests',
]

MEDIA_URL = '/media/'

MEDIA_ROOT = local_path('media')

SECRET_KEY = "app-test"

TEMPLATE_DIRS = (
    local_path('templates'),
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'survey.urls'
