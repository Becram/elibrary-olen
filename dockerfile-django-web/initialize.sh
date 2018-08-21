#!/bin/bash
set -e

python manage.py migrate --settings=pustakalaya.settings.production >> /dev/stdout 2>&1 &&

python manage.py index_pustakalaya --settings=pustakalaya.settings.production >> /dev/stdout 2>&1 &&

python manage.py collectstatic --settings=pustakalaya.settings.production   --noinput >> /dev/stdout 2>&1
