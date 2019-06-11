import os
import sys
import yaml
import logging
import boto3
import pandas as pd
sys.path.append(os.path.join('../../'))
import src.generate_features

# set up logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# pull specified configurations from YAML file
with open('../../config/config.yml', "r") as f:
    config = yaml.load(f)

# UNIT TEST to validate features were loaded from s3 into S3 and values are in the expected range 
def test_generate_features():

    # pull required attributes from config
    s3_bucket = config["generate_features"]["s3_bucket"]
    s3_raw = config["generate_features"]["s3_features"]

    #import data from s3
    s3 = boto3.client('s3')
    logging.info('Unit Test: Connecting to S3 bucket for data %s', s3_bucket)
    obj = s3.get_object(Bucket=s3_bucket, Key=s3_raw)
    logging.info('Unit Test: Read file from s3 bucket %s', s3_raw)
    data = pd.read_csv(obj['Body']) # return as df

    # UNIT TEST: check count of features to ensure dummy variables got created in generate features
    assert len(data.columns) == 15

    # UNIT TEST: check that all rows are still present
    assert len(data.index) == 303