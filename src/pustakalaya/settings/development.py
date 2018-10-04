from .base import *  # NOQA

DEBUG = True

#100MB
FILE_UPLOAD_MAX_MEMORY_SIZE=104857600

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

        #---Sqlite settings
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        #---Postgres settings
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pustakalaya',
        'USER': 'pustakalaya_user',
        'PASSWORD': 'pustakalaya123',
        'HOST': 'pgmaster',
        'PORT': '5432',
    }
}
