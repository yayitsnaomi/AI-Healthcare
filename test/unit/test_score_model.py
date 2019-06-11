import os
import sys
import yaml
import logging
import boto3
import pandas as pd
sys.path.append(os.path.join('../../'))
import src.score_model as sm

# set up logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# pull specified configurations from YAML file
with open('../../config/config.yml', "r") as f:
    config = yaml.load(f)

# UNIT TEST to validate model is working properly and returning above expected accuracy threshold
def test_score_model():
    # get S3 data to test
    s3_bucket = config["score_model"]["s3_bucket"]
    s3_features = 'results/CV_mean.csv'
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=s3_bucket, Key=s3_features)
    logging.info('UNIT TEST: get data from s3 bucket & validate mean score %s', s3_features)
    mean =  pd.read_csv(obj['Body'])
    assert mean.iloc[0][0] > .75 # check mean value is > accuracy expected threshold