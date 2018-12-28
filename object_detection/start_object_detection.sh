#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/notebooks/models/research:/notebooks/models/research/slim

# retrained based on SSD_MobileNet_V1
HOMEDIR=/notebooks/object_detection
PIPELINE_CONFIG_PATH=$HOMEDIR/ssd_mobilenet_v1_fruit/pipeline.config
CUS_PIPELINE_CONFIG_PATH=${HOMEDIR}/data/pipeline.config
MODEL_DIR=$HOMEDIR/model
NUM_TRAIN_STEPS=20000
SAMPLE_1_OF_N_EVAL_EXAMPLES=1
RUNDIR=/notebooks/models/research

# customize pipeline.config
# generate a CONFIG_PATH inside folder data/
python ${HOMEDIR}/helpers/set_training_configuration.py \
    --you_own True \
    --label_map ${HOMEDIR}/data/label_map.pbtxt \
    --pipeline ${PIPELINE_CONFIG_PATH} \
    --pipelineoutput ${CUS_PIPELINE_CONFIG_PATH}
if [ ! -e ${CUS_PIPELINE_CONFIG_PATH} ]; then
    echo "Training configuration was not generated. Training was stopping."
    exit 1
fi
echo "Customized pipeline config was generated successfully."

# start tensorboard
bash ${HOMEDIR}/start_tensorboard.sh

# retrain 
echo "Start a object detection retraining."
cd ${RUNDIR}
python object_detection/model_main.py \
    --pipeline_config_path=${CUS_PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=${SAMPLE_1_OF_N_EVAL_EXAMPLES} \
    --alsologtostderr
echo "Training finished."

# copy the label file from pipeline.config
echo "Copy the label file."
label_path=`python ${HOMEDIR}/helpers/parser.py --method labelfile --pipeline ${PIPELINE_CONFIG_PATH}`
cp ${label_path} ${MODEL_DIR}/label_map.pbtxt

# export frozen model
echo "Freeze the model."
bash ${HOMEDIR}/helpers/export_object_detection_model.sh

exit 0