#!/bin/bash
check_non_empty() {
  # $1 is the content of the variable in quotes e.g. "$FROM_EMAIL"
  # $2 is the error message
  if [[ "$1" == "" ]]; then
    echo "ERROR: specify $2"
    exit -1
  fi
}


check_exec_success() {
  # $1 is the content of the variable in quotes e.g. "$FROM_EMAIL"
  # $2 is the error message
  if [[ "$1" != "0" ]]; then
    echo "ERROR: $2 failed"
    echo "$3"
    exit -1
  fi
}


CurDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LogDir=/data/so-dashboard/log
TmpDir=/data/so-dashboard/tmp
UwsgiLogDir=/data/so-dashboard/log/uwsgi

mkdir -p $LogDir
mkdir -p $TmpDir
mkdir -p $UwsgiLogDir

BaseImage="daocloud.io/rolight/so-dashboard:master-e95edd4"

if [[ -a ${CurDir}/envs.sh ]]; then
  source ${CurDir}/envs.sh
fi

DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-dashboard.settings.default}

# get host ip
# HostIP="$( python -c "import socket; print(socket.gethostbyname(socket.gethostname()))" )"
# echo $HostIP > localaddr.ini

runserver(){
    export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
    python manage.py runserver
}

create_data_volume(){
  docker inspect so-dashboard-data &> /dev/null
  if [[ "$?" == "1" ]]; then
    docker create --name so-dashboard-data \
      -v ${CurDir}:/usr/src/app \
      -v ${LogDir}:/usr/src/app/logs \
      -v ${TmpDir}:/usr/src/app/tmp \
      alpine /bin/true

    docker run --rm --volumes-from so-dashboard-data \
      ${BaseImage} mkdir -p logs/uwsgi/ logs/cron/
  fi

}

start() {

  docker kill so-dashboard 2>/dev/null
  docker rm -v so-dashboard 2>/dev/null

  create_data_volume

  docker run -d --name so-dashboard \
    -e "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" \
    -p 9039:9039 \
    --volumes-from so-dashboard-data \
    --restart=always \
    --log-opt max-size=10m \
    --log-opt max-file=9 \
    ${BaseImage} \
    uwsgi --ini /usr/src/app/dashboard/uwsgi.ini

  check_exec_success "$?" "start so-dashboard container"

  docker run --rm --volumes-from so-dashboard-data \
    -e "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" \
    --net=host \
    ${BaseImage} python3 manage.py migrate

}

stop() {
  docker stop so-dashboard 2>/dev/null
  docker rm -v so-dashboard 2>/dev/null
  docker rm -v so-dashboard-data 2>/dev/null
}

reload() {
  docker run --rm --volumes-from so-dashboard-data \
    -e "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" \
    --net=host \
    ${BaseImage} python3 manage.py migrate
  docker kill -s HUP so-dashboard
}

shell() {
  create_data_volume

  docker run --rm -it \
    -e "LANG=C.UTF-8" \
    -e "DJANGO_SETTINGS_MODULE=dashboard.settings.default" \
    --volumes-from so-dashboard-data \
    --net=host \
    ${BaseImage} \
    bash
}

test() {
  create_data_volume

  docker run --rm -it \
    -e "DJANGO_SETTINGS_MODULE=dashboard.settings.test" \
    -e "LANG=C.UTF-8" \
    --volumes-from so-dashboard-data \
    --net=host \
    ${BaseImage} \
    python manage.py test "$@"
}


manage() {
  create_data_volume
  docker run --rm -it \
    -e "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" \
    -e "LANG=C.UTF-8" \
    --volumes-from so-dashboard-data \
    --net=host \
    ${BaseImage} \
    python manage.py $@
}

init() {
    manage migrate
    manage createsuperuser
}

cron() {
  docker stop so-dashboard-cron 2>/dev/null
  docker rm -vf so-dashboard-cron 2>/dev/null

  create_data_volume

  action=${1:-start}
  case $action in
    stop) exit ;;
    start)
      docker run -d --name so-dashboard-cron \
        --volumes-from so-dashboard-data \
        -e "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" \
        -e "TZ=Asia/Shanghai" \
        --restart=always \
        --log-opt max-size=10m \
        --log-opt max-file=9 \
        ${BaseImage} \
        python -u cron.py
      ;;
  esac
}


##################
# Start of script
##################

Action=$1

shift

case "$Action" in
  start) start "$@";;
  stop) stop ;;
  restart)
    stop
    start
    ;;
  reload) reload "$@" ;;
  shell) shell "$@" ;;
  test) test "$@" ;;
  manage) manage "$@" ;;
  runserver) runserver ;;
  cron) cron "$@" ;;
  init) init ;;
  *)
    echo "Usage:"
    echo "./dashboard.sh start|stop|restart"
    echo "./dashboard.sh reload [full]"
    echo "./dashboard.sh shell"
    echo "./dashboard.sh manage"
    echo "./dashboard.sh cron"
    echo "./dashboard.sh init"
    exit 1
    ;;
esac

exit 0
