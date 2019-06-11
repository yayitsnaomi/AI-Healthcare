import os
import sys
import yaml
import logging
import boto3
import pandas as pd
sys.path.append(os.path.join('../../'))
import src.train_model as tm

# set up logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# pull specified configurations from YAML file
with open('../../config/config.yml', "r") as f:
    config = yaml.load(f)

# UNIT TEST to validate test /train splits working as expected 
def test_build_model():

    # load data from s3
    data = tm.gets3data(config["train_model"]["s3_bucket"], config["train_model"]["s3_features"])

    # build model & review feature importance
    logging.info('Testing build model and generating test / train splits')
    model, x_test, y_test = tm.build_model(config["train_model"]["s3_bucket"], data, config["train_model"]["test_size"])

    # UNIT TEST: check rows and columns of x_test
    assert len(x_test.columns) == 13
    assert len(x_test.index) == 91 # 303*.3 = 91 in test set

    # UNIT TEST: check rows and columns of y_test
    assert len(y_test.columns) == 1
    assert len(y_test.index) == 91  # 303*.3 = 91 in test set