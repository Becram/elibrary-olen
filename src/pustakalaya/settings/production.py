from .base import *  # NOQA

DEBUG = True

#CELERY_BROKER_URL = 'amqp://rabbitmq'

try:
    db_name = config["DATABASE"]["NAME"]
    db_user = config["DATABASE"]["USER"]
    db_password = config["DATABASE"]["PASSWORD"]
    db_host = config["DATABASE"]["HOST"]
    db_port = config["DATABASE"]["PORT"]
except KeyError:
    raise ImproperlyConfigured("Improperly configured database settings.")

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pustakalaya',
        'USER': 'pustakalaya_user',
        'PASSWORD': 'pustakalaya123',
        'HOST': 'db',
        'PORT': '5432',
    }
}
