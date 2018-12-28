#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/notebooks/models/research:/notebooks/models/research/slim

DATA_PATH=/notebooks/object_detection/data
TRAINED_PATH=/notebooks/object_detection/model
HELPERS_DIR=/notebooks/object_detection/helpers

# get the latest checkpoint
latest=`python ${HELPERS_DIR}/parser.py --method lastestCheckpoint --ckpt ${TRAINED_PATH}`

# check whether pre-exported model exists
SAVED_MODEL_PATH=${TRAINED_PATH}/saved_model
if [ -d ${SAVED_MODEL_PATH} ]; then
   rm -rf ${SAVED_MODEL_PATH}
fi

# export the frozen model
# trained_checkpoint_prefix: can be model.ckpt or model.ckpt-10000, etc.
cd /notebooks/models/research
python object_detection/export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path ${DATA_PATH}/pipeline.config \
    --trained_checkpoint_prefix ${latest} \
    --output_directory ${TRAINED_PATH}
echo "Export a frozen model completely."

# copy label file
cp ${DATA_PATH}/label_map.pbtxt ${TRAINED_PATH}
