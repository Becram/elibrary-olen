#!/usr/bin/env bash

SCRIPT_SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
TEMP=/tmp/pustakalaya
BACKUP_SRC=sysadmin@pustakalaya.org:/library/backup/postgres_backup/daily/pustakalaya/*
# BACKUP_SRC=/library/backup/postgres_backup/daily/pustakalaya/*
mkdir -p $TEMP
rsync -aP --delete $BACKUP_SRC  $TEMP

backup_file_bz2=$(ls $TEMP | tail -n 1)

pushd  $TEMP
if [[ -f $backup_file_bz2 ]] ; then
     bzip2 -dk $backup_file_bz2
     if [ $? -eq 0 ]; then
          echo "removing old file"
          rm -rfv $SCRIPT_SRC/dockerfile-postgres-master/*.sql

          echo "moving file $TEMP/${backup_file_bz2%.*} to  $SCRIPT_SRC/dockerfile-postgres-master/ "
          mv $TEMP/${backup_file_bz2%.*}  ${SCRIPT_SRC}/dockerfile-postgres-master/

     else
           echo " Error decompressing bzip2 file"
     fi


else
     echo "backup file $backup_file_bz2 not found"
fi
popd
