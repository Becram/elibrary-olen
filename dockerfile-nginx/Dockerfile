FROM becram/olen_elib_nginx:v1.1

MAINTAINER Bikram Dhoju <bikram.dhoju@olenepal.org>

COPY etc/nginx/conf.d/nginx.conf /etc/nginx/conf.d/nginx.conf

COPY etc/nginx/nginx.conf /etc/nginx/nginx.conf

#Set timezone
ENV TZ=Asia/Kathmandu
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
