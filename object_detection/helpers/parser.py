#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jiankaiwang
@usage:
    python parser.py --method lastestCheckpoint --ckpt /ssd_mobilenet_v1_coco
    python parser.py --method labelfile --pipeline /ssd_mobilenet_v1_coco/pipeline.config
"""

import argparse

import sys
sys.path.append("/notebooks/models/research")
from object_detection.utils import config_util
from object_detection.utils import label_map_util

# In[]

def lastestCheckpoint(CKPT_PATH):
    """
    description: Get the latest checkpoint path from a training folder.
    input:
        CKPT_PATH: the folder path
    """
    import tensorflow as tf
    latest_ckpt = tf.train.latest_checkpoint(CKPT_PATH)
    return "{}".format(latest_ckpt)

# In[]

def getConfigFromPipeline(PIPELINE_PATH):
    try:
        content = config_util.get_configs_from_pipeline_file(PIPELINE_PATH)
        return content, False
    except Exception as e:
        content = None
        print(str(e))
        return content, True
    
# In[]

def getLabelFilePath(PIPELINE_PATH):
    """
    description: Get the label file path for training.
                 It is the same with valid and inference in general.
    input:
        CKPT_PATH: the folder path
    """
    content = config_util.get_configs_from_pipeline_file(PIPELINE_PATH)
    return content["train_input_config"].ListFields()[0][1]

# In[]

def getClassNumber(PIPELINE_PATH):
    content, err = getConfigFromPipeline(PIPELINE_PATH)
    if not err:
        try:
            return config_util.get_number_of_classes(content["model"]), False
        except Exception as e:
            return str(e), True
    else:
        return "Parsing configuration file is error.", True

# In[]
    
def getNumberClassInLabelMap(LABLE_PATH):
    category_index = label_map_util.create_category_index_from_labelmap(\
        LABLE_PATH, use_display_name=True)
    return category_index

# In[]
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
      
    parser.add_argument('--method', type=str, default=None, help='methods')
    parser.add_argument('--ckpt', type=str, default=None, help='ckpt path')
    parser.add_argument('--pipeline', type=str, default=None, help='pipe path')

    args = parser.parse_args()
    
    METHOD = args.method
    CKPT_PATH = args.ckpt
    PIPE_PATH = args.pipeline
    
    assert METHOD is not None, "Method (--method) is required."
        
    if METHOD == "lastestCheckpoint":
        assert CKPT_PATH is not None, "Checkpoint (--ckpt) path is required."
        print(lastestCheckpoint(CKPT_PATH))
        
    elif METHOD == "labelfile":
        assert PIPE_PATH is not None, "Pipeline (--pipeline) path is required."
        print(getLabelFilePath(PIPE_PATH))























        