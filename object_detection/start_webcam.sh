#/bin/bash

WORKDIR=/notebooks/Flask_Video_Streaming_for_Object_Detection

cd ${WORKDIR}
export CAMERA=obdet 
gunicorn --worker-class gthread --threads 5 --workers 1 --bind 0.0.0.0:5000 app:app
echo $! > /tmp/obdet.run