#!/bin/bash

set +x
HOST=$(ifconfig enp1s0 | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1)
LOCAL_BACKUP="/library/backup_pg_pustakalaya/backup/daily/pustakalaya"

if [ $# -ne 1 ] ; then
 echo "Usage: $0 command" >&2 ; exit 1
fi


# runs as root or needs sudo?
if [[ "$EUID" -ne 0 ]]; then
  sudo='sudo'
else
  sudo=''
fi

# Checking if docker and docker-compose has been pre installed or not
# echo "Checking if docker and docker-compose has been pre installed or not"
function program_is_installed {
    # set to 1 initially
    local return_=1
    # set to 0 if not found
    type $1 >/dev/null 2>&1 || { local return_=0; }
    # return value
    echo $return_
}


if [ $(program_is_installed "docker") -eq 0 ] || [ $(program_is_installed "docker-compose") -eq 0 ] ; then
    die "Docker and/or Docker-compose does not seem to be installed in the system. Please install it"

fi


showLoading() {
   mypid=$!
   loadingText="Running"

   echo -ne "$loadingText\r"

  while kill -0 $mypid 2>/dev/null; do
    echo -ne "$loadingText.\r"
    sleep 0.5
    echo -ne "$loadingText..\r"
    sleep 0.5
    echo -ne "$loadingText...\r"
    sleep 0.5
    echo -ne "\r\033[K"
    echo -ne "$loadingText\r"
    sleep 0.5
  done

  echo "$loadingText...FINISHED"
}

process() {
    if [ $# -eq 1 ] && ([ "$1" = "-h" ] || [ "$1" = "--help" ]); then
        show_help
    else
        # launch_containers

        while true; do
            case $1 in
                "-b" | "--build")
                    docker_rebuild_images
                    shift
                    ;;
                "-up" | "--composer-up")
                    docker_up
                    shift
                    ;;
                "--dump" )
                    docker_dump_sql
                    shift
                    ;;
                "--index" )
                    docker_index
                    shift
                    ;;
                "--remove")
                    composer_remove
                    shift
                    ;;
                "--composer-update")
                    run_composer_update
                    shift
                    ;;
              "--production")
                    showLoading
                    # echo "Backing up"
                    # docker_backup_local
                    echo "Removing containers"
                    docker_remove
                    echo "Building containers"

                    docker_rebuild_images 
                    echo "Waiting...."
                    sleep  20
                    echo "Dumping database"
                    docker_dump_sql &> /dev/null
                    echo "Indexing"
                    docker_index
                    echo "collecting statics"
                    docker_collectstatic | grep "static files copied"

                    shift
                        ;;
                * ) break ;;
            esac
        done

        echo -e "\n\nEpustakalya deployed and can be accessed from http://$HOST."
    fi
}

launch_containers() {
    docker-compose up -d
}

docker_rebuild_images() {
     docker-compose build && launch_containers
}

docker_up() {
    docker-compose up -d
}

docker_prune_system() {
    docker system prune -a -f
}

docker_remove() {
    docker-compose stop && docker-compose rm -f
}

docker_backup_local(){
#     docker exec postgres_01 bash -c "/script/autopgsqlbackup "
container="postgres_01"
if [ $(docker inspect -f '{{.State.Running}}' $container) = "true" ]; then
      echo "getBack up of postgres"
      docker exec postgres_01 bash -c "/script/autopgsqlbackup";
      echo "Successfully backed up to fileserver"
else
      echo "Container $container is not running";
fi
}
docker_index(){
     docker exec django_web_01 bash -c "python manage.py index_pustakalaya --settings=pustakalaya.settings.production"

}

docker_collectstatic(){
  docker exec django_web_01 bash -c "python manage.py collectstatic --settings=pustakalaya.settings.production --noinput"

}
docker_migrate(){
  docker exec django_web_01 bash -c "python manage.py migrate --settings=pustakalaya.settings.production"

}

docker_dump_sql(){
  backup_file_bz2=$(ls $LOCAL_BACKUP | tail -n 1 )
  echo "backup file is $backup_file_bz2"
  pushd $LOCAL_BACKUP
  if [[ -f $backup_file_bz2 ]] ; then
      bzip2 -dk $backup_file_bz2
      backup_file_sql=${backup_file_bz2%.*}
      # container="postgres_01"
      # CMD="psql --username pustakalaya_user -d pustakalaya -f /pg_backups/backup/daily/pustakalaya/$backup_file_sql"
      # run_in_conatiner $container $CMD
      docker exec postgres_01 bash -c "psql --username pustakalaya_user -d pustakalaya -f /pg_backups/backup/daily/pustakalaya/$backup_file_sql"
      if [ $? -eq 0 ]; then
          echo "Dumpped  from $backup_file_sql"
          rm -rvf $LOCAL_BACKUP/*sql
      else
          echo "Failed Dumping file"
      fi
  else
     echo "No backup file found at $LOCAL_BACKUP. Please backup first"
  fi
     popd

}

run_in_conatiner(){
   docker exec $1 bash -c $2

}

docker_exec(){
    docker exec -it $1 /bin/bash
}

show_help() {
    echo -e "-b, --b" \
        "\n\t Rebuild the docker images" \
        "\n-i, --composer-install" \
        "\n\t Run composer-install" \
        "\n-u, --composer-update" \
        "\n\t Run composer-update" \
        "\n-h, --help" \
        "\n\t Display this help and exit"
}

process "$@"
