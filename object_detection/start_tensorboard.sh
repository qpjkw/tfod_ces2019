#/bin/bash

BASEDIR=/notebooks/object_detection
LOGDIR=${BASEDIR}/model

if [ -e '/tmp/tfb.run' ]; then
    bash ${BASEDIR}/stop_tensorboard.sh
fi

echo "Start Tensorboard."
tensorboard --logdir=${LOGDIR} > /dev/null 2>&1 & 
echo $! > /tmp/tfb.run