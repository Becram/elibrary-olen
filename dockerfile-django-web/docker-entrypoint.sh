#!/bin/bash
set -e

if [ -f ./entrypoint-pre.sh ]; then
    ./entrypoint-pre.sh
fi

args=("$@")

case $1 in
    manage)
        export DJANGO_SETTINGS_MODULE=pustakalaya.settings.production
        exec python manage.py ${args[@]:1}
        ;;
    run)
        export DJANGO_SETTINGS_MODULE=pustakalaya.settings.production
        exec gunicorn ${DJANGO_WSGI_MODULE}:application --name $GUNICORN_NAME --workers $GUNICORN_NUM_WORKERS --user=$APP_USER   -b 0.0.0.0:8001 --timeout=90 --log-file=/var/log/gunicorn-error.log
        # sleep 60 && ./entrypoint-post.sh
        ;;
    develop-manage)
        export DJANGO_SETTINGS_MODULE=pustakalaya.settings.development
        exec python manage.py ${args[@]:1}
        ;;
    develop-run)
        export DJANGO_SETTINGS_MODULE=pustakalaya.settings.development
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    *)
        if [ -f ./entrypoint-extras.sh ]; then
            ./entrypoint-extras.sh
        else
            exec "$@"
        fi
        ;;
esac
