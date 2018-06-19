#!/bin/bash

set +x
#HOST=$(ifconfig enp1s0 | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1)
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
                "--up" | "--composer-up")
                    docker_up
                    shift
                    ;;
                "--backup" )
                    notify "get backup"
                    docker_backup_local

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
              "--development")
                  notify "Backing up"
                  docker_backup_local "dev"
                  notify "Removing containers"
                  docker_remove "prod"

                  # notify "Deletelting UNTAGGED images"
                  # docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
                  notify "Building containers"
                  docker_rebuild_images "dev"
                  notify "Lauching container"
                  docker_up "dev"
                  notify "Dumping database"
                  docker_dump_sql "prod"
                  notify "Migrating django DB"
                  docker_migrate "dev"
                  notify "Indexing"
                #  docker_index
		              docker exec dev_django_web_01 bash -c "python manage.py index_pustakalaya --settings=pustakalaya.settings.production"
                  get_deploy_version
		              notify "Collecting statics"
                  docker_collectstatic "dev" | grep "static files copied"

                  shift
                  ;;
              "--production")
                    # showLoading
                    notify "Deploying in Production Mode"
                    # docker_backup_local
                    notify "Removing containers"
                    docker_remove "prod"
                    notify "Bringing up conatiners"
                    docker_up "prod"
                    # notify "Building containers"
                    #
                    # docker_rebuild_images
                    notify "Waiting...."
                    sleep  20
                    notify "Dumping database"
                    docker_dump_sql "prod"
                    notify "Migrating django DB"
                    docker_migrate "prod"

                    notify "Indexing"
                    docker_index "prod"
		                get_deploy_version
                    notify "collecting statics"
                    docker_collectstatic "prod" | grep "static files copied"

                    shift
                        ;;
                * ) break ;;
            esac
        done

       echo -e "\n\nEpustakalya deployed Successfully."
    fi
}



#####################################################################
#Logging from
#####################################################################
PROGNAME=$(basename $0)

function error_exit
{

#   ----------------------------------------------------------------
#   Function for exit due to fatal program error
#       Accepts 1 argument:
#           string containing descriptive error message
#   ----------------------------------------------------------------

    echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
    exit 1
}

notify() { log "LOG: $1"; }
log() {
        RED='\033[0;31m'
        NC='\033[0m'
        exec 3>&2
        datestring=`date +'%Y%m%d%H:%M:%S'`
        # Expand escaped characters, wrap at 70 chars, indent wrapped lines
        echo -e "$datestring ${RED}$1${NC}" | fold -w70 -s | sed '2~1s/^/  /' >&3
}

get_release() {
    # Does this commit have an associated release tag?
    git tag --points-at HEAD | tail -n1 2>/dev/null |
       sed -e 's/^release-//'

}

release_is_number() {
    get_release | grep -Eqx "[0-9]+"
}

get_deploy_version(){

DATE=`date '+%Y%m%d%H%M%S'`

sed -i "s/^v1.0.*/v1.0-$DATE/g" src/templates/static_pages/about.html

}


make_name() {
    prefix="EP"
    release=$(get_release)

    if [ -z "$release" ]; then
        log "No release tag found; quitting"
    fi

    name=$prefix-$release
}



docker_rebuild_images() {
     docker-compose -f docker-compose-$1.yml build
}

docker_stop(){
         docker-compose -f docker-compose-$1.yml stop
}

docker_up() {
    docker-compose -f docker-compose-$1.yml up -d
}

docker_prune_system() {
    docker system prune -a -f
}

docker_remove() {
    docker-compose -f docker-compose-"$1".yml stop && docker-compose -f docker-compose-"$1".yml rm -f
}

docker_backup_local(){
#     docker exec postgres_01 bash -c "/script/autopgsqlbackup "
container="$1_postgres_01"
if [ $(docker inspect -f '{{.State.Running}}' $container) = "true" ]; then
      echo "getBack up of postgres"
      docker exec $1_postgres_01 bash -c "/script/autopgsqlbackup";
      echo "Successfully backed up"
else
      echo "Container $container is not running";
fi
}
docker_index(){
     docker exec "$1"_django_web_01 bash -c "python manage.py index_pustakalaya --settings=pustakalaya.settings.production"

}

docker_collectstatic(){
  docker exec "$1"_django_web_01 bash -c "python manage.py collectstatic --settings=pustakalaya.settings.production --noinput"

}
docker_migrate(){
  docker exec "$1"_django_web_01 bash -c "python manage.py migrate --settings=pustakalaya.settings.production"

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
      docker exec "$1"_postgres_01 bash -c "psql --username pustakalaya_user -d pustakalaya -f /pg_backups/backup/daily/pustakalaya/$backup_file_sql"
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
