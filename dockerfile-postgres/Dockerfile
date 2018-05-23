FROM postgres:9.6

ENV APP_ROOT /src
ENV BACKUP_DIR /library/backup_pg_pustakalaya/backup/daily/pustakalaya/

WORKDIR ${APP_ROOT}
#RUN mkdir -p  /script && > /etc/cron.d/pg_backup-cron && echo "*/5 * * * * /script/autopgsqlbackup" >> /etc/cron.d/pg_backup-cron
RUN mkdir -p $BACKUP_DIR
ADD autopgsqlbackup /script/
ADD *.bz2 $BACKUP_DIR
RUN chmod +x /script/autopgsqlbackup
