FROM python:3.6.5
ENV PYTHONUNBUFFERED 1

#ENV C_FORCE_ROOT true

ENV APP_USER myapp
ENV APP_ROOT /src
RUN mkdir /src
#RUN groupadd -r ${APP_USER} \
#    && useradd -r -m \
#    --home-dir ${APP_ROOT} \
#    -s /usr/sbin/nologin \
#    -g ${APP_USER} ${APP_USER}
#
RUN adduser --disabled-password --gecos '' ${APP_USER}
WORKDIR ${APP_ROOT}



RUN mkdir -p /library/media_root
RUN mkdir -p  /library/static_root
RUN mkdir /config
ADD src/requirements/requirements_dev.txt /config/
ADD src/requirements/base.txt /config/
ADD src/requirements/requirements_prod.txt /config/
RUN pip install -r /config/requirements_prod.txt

#Sass installation
RUN apt-get update -y && apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_9.x | bash
RUN apt-get install nodejs -y
RUN npm install gulp -g
#RUN gulp sass
#RUN gulp sass

#Set timezone
ENV TZ=Asia/Kathmandu
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN chown -R ${APP_USER}:${APP_USER} /library/media_root
RUN chown -R ${APP_USER}:${APP_USER} /library/static_root
RUN chown -R ${APP_USER}:${APP_USER} /src
RUN chown -R ${APP_USER}:${APP_USER} /var/log

# to fix the issue of docker host name web in confirm url
COPY ./dockerfile-django-web/adapter.py /usr/local/lib/python3.6/site-packages/allauth/account/adapter.py

EXPOSE 8000

USER ${APP_USER}

ADD . ${APP_ROOT}
