#!/bin/sh


function _term() {
  echo "Caught SIGTERM signal!"
  kill $pid
  exit 0
}


cd /app/krake
python manage.py runserver 0:8000 &
# save logutil PID
pid="$!"
# wait forever or a SIGNAL
trap _term SIGTERM
while true
do
    wait $pid
done
