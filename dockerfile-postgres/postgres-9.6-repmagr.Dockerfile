FROM postgres:9.6
MAINTAINER Bikram Dhoju <bikram.dhoju@olenepal.org>

ENV PG_MAX_WAL_SENDERS 8
ENV PG_WAL_KEEP_SEGMENTS 8

RUN apt-get update --fix-missing -y && apt-get install -y iputils-ping postgresql-client


ADD backups-cron /etc/cron.d/backups-cron
RUN touch /var/log/cron.log
ADD backups.sh /backups.sh
ADD start.sh /start.sh

COPY setup-replication.sh /docker-entrypoint-initdb.d/
COPY docker-entrypoint.sh /docker-entrypoint.sh

COPY *sql  /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/setup-replication.sh /docker-entrypoint.sh
