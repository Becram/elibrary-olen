#!/bin/bash


export PYTHONUNBUFFERED=1


# wait for postges
echo "Waiting for postgresql database"
while true
do
  if ! [ -z "${DJANGO_NOWAIT}" ]; then
    break
  fi

  curl -s http://${DJANGO_DATABASE_HOST}:5432
  if [ "$?" = "0" -o  "$?" = "52" ]; then
    break
  fi
  echo "$(date) - still trying"
  sleep 10
done

# if [ "DJANGO_DATABASE_HOST" = "pgmaster" ]; then
#     sleep 10 # wait for dockerized postgress will warm up
# fi

echo "$(date) - connected successfully"


python manage.py migrate --settings=${DJANGO_SETTINGS_MODULE} >> /dev/stdout 2>&1 &&

python manage.py index_pustakalaya --settings=${DJANGO_SETTINGS_MODULE} >> /dev/stdout 2>&1  &&



python manage.py collectstatic --settings=${DJANGO_SETTINGS_MODULE}   --noinput >> /dev/stdout 2>&1
# django-admin migrate --noinput
# django-admin collectstatic --noinput

# # for PyCharm remote python interpretator
# if ! [ -z "${DJANGO_DEV}" ]; then
#     /usr/sbin/sshd
# fi

if ! [ -z "${DJANGO_DEBUG}" ]; then
    django-admin runserver 0.0.0.0:8001
else
    gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $GUNICORN_NAME \
    --workers $GUNICORN_NUM_WORKERS \
    --user=$APP_USER  \
    -b 0.0.0.0:8001 \
    --timeout=90 \
    --log-file=/var/log/gunicorn-error.log
fi
