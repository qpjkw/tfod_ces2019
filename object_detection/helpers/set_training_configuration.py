#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jiankaiwang
@usage:
    python set_training_configuration.py \
        --you_own True \
        --label_map /notebooks/object_detection/data/label_map.pbtxt \
        --pipeline /notebooks/object_detection/ssd_mobilenet_v1_coco_2018_01_28_docker/pipeline.config \
        --pipelineoutput /notebooks/object_detection/data/pipeline.config \
"""

# In[]

import argparse
import os
import sys
sys.path.append("/notebooks/models/research")

import tensorflow as tf

from google.protobuf import text_format
from object_detection.utils import config_util
import parser

# In[]

def set_num_class(LMAP_PATH, PIPE_PATH, OUTPUT_PATH):
    number, err = parser.getClassNumber(PIPE_PATH)
    
    if not err:
        try:
            data = parser.getNumberClassInLabelMap(LMAP_PATH)
        except Exception as e:
            raise Exception(str(e))
            return "Parsing the label file is error.", True
    else:
        return "Parsing the config file is error.", True
    
    content, err = parser.getConfigFromPipeline(PIPE_PATH)
    if number != len(data):
        if err: return "Parsing the configuration file is error.", True
        content["model"].ssd.num_classes = len(data)
    
    return content, False

# In[]

def write_new_config(config, OUTPUT_PATH):
    """
    description: 
    input:
        config: a dict-based config
    """
    try:
        pipeline_config_msg = config_util.create_pipeline_proto_from_configs(config)    
        pipeline_config_final = text_format.MessageToString(pipeline_config_msg)
        with tf.gfile.Open(OUTPUT_PATH, "wb") as f:
            f.write(pipeline_config_final)
        return None, False
    except Exception as e:
        return str(e), True

# In[]

if __name__ == "__main__":
    
    pas = argparse.ArgumentParser()

    pas.add_argument('--you_own', type=str, default="False", help='use your own data')
    pas.add_argument('--label_map', type=str, default="", help='label map path')
    pas.add_argument('--pipeline', type=str, default="", help='pipe template path')
    pas.add_argument('--pipelineoutput', type=str, default="", help='pipe output path')

    args = pas.parse_args()
    
    if str(args.you_own) == "True":
        LMAP_PATH = args.label_map
        PIPE_PATH = args.pipeline
        OUTPUT_PATH = args.pipelineoutput
    else:
        model_path = "/notebooks/object_detection"
        LMAP_PATH = os.path.join(model_path, "data", "label_map.pbtxt")
        PIPE_PATH = os.path.join(model_path, "ssd_mobilenet_v1_coco_2018_01_28_docker", "pipeline.config")
        OUTPUT_PATH = os.path.join(model_path, "data", "pipeline.config")
    
    assert os.path.exists(LMAP_PATH), "Label map file is not found."
    assert os.path.exists(PIPE_PATH), "Pipeline template file is not found."

    content, err = set_num_class(LMAP_PATH, PIPE_PATH, OUTPUT_PATH)
    if err: print(content)
    msg, err = write_new_config(content, OUTPUT_PATH)
    if err: print(msg)
    sys.exit(err)
    

