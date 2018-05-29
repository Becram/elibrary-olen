FROM python:latest
ENV PYTHONUNBUFFERED 1

#ENV C_FORCE_ROOT true

ENV APP_USER myapp
ENV APP_ROOT /src
ENV PROJECTDIR /src
#ENV SOCKFILE $PROJECTDIR/gunicorn.sock
#ENV DJANGO_SETTINGS_MODULE pustakalaya.settings.production
#ENV DJANGO_WSGI_MODULE pustakalaya.wsgi
#
#RUN export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE && export PYTHONPATH=$DJANGODIR:$PYTHONPATH



RUN mkdir /src
#RUN groupadd -r ${APP_USER} \
#    && useradd -r -m \
#    --home-dir ${APP_ROOT} \
#    -s /usr/sbin/nologin \
#    -g ${APP_USER} ${APP_USER}
#

RUN adduser --disabled-password --gecos '' ${APP_USER}

WORKDIR ${APP_ROOT}

RUN mkdir /config
ADD src/requirements/requirements_dev.txt /config/
ADD src/requirements/base.txt /config/
ADD src/requirements/requirements_prod.txt /config/
RUN pip install -r /config/requirements_prod.txt
RUN apt-get update && apt-get install poppler-utils -y

#COPY ./script.d/run_celery  /src/script.d/
#RUN chmod +x /src/script.d/run_celery

#RUN chown -R ${APP_USER}:${APP_USER} /src
EXPOSE 8000
ADD . ${APP_ROOT}
#Set timezone 
ENV TZ=Asia/Kathmandu
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

USER ${APP_USER}

#CMD ["celery", "-A", "pustakalaya", "worker", "-l", "info"]


#CMD ["/src/script.d/run_celery"]
