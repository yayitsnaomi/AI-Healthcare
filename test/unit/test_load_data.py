import os
import sys
import yaml
import logging
import boto3
import pandas as pd
sys.path.append(os.path.join('../../'))
print(sys.path)
import src.load_data

# set up logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# pull specified configurations from YAML file
with open('../../config/config.yml', "r") as f:
    config = yaml.load(f)

# UNIT TEST to validate features were loaded from RDS into S3 and values are in the expected range 
def test_load_data():

    # pull required attributes from config
    s3_bucket = config["load_data"]["s3_bucket"]
    s3_raw = config["load_data"]["s3_clean"]

    #import data from s3
    s3 = boto3.client('s3')
    logging.info('Unit Test: Connecting to S3 bucket for data %s', s3_bucket)
    obj = s3.get_object(Bucket=s3_bucket, Key=s3_raw)
    logging.info('Unit Test: Read file from s3 bucket %s', s3_raw)
    data = pd.read_csv(obj['Body']) # return as df

    # count errors
    count = 0

    #Check all rows for NULLs
    if data.isnull().values.any() == True:
        logging.info('Loading Error: NULL VALUES IN RAW DATA!!!')
        count= count+1

    #Check all rows for range of values
    elif (max(data['age']) > 100 or min(data['age']) < 1):
        logging.info('Loading Error: PATIENT AGE OUT OF RANGE BOUNDS!!!')
        count= count+1

    #Check ranges of input values make sense
    elif (max(data['trestbps']) > 205 or min(data['trestbps']) < 90):
        logging.info('Loading Error: trestbps OUT OF RANGE BOUNDS!!!')
        count= count+1

    elif (max(data['chol']) > 570 or min(data['chol']) < 120):
        logging.info('Loading Error: chol OUT OF RANGE BOUNDS!!!')
        count= count+1

    elif (max(data['thalach']) > 202 or min(data['thalach']) < 70):
        logging.info('Loading Error: thalach OUT OF RANGE BOUNDS!!!')
        count= count+1

    elif (min(data['oldpeak']) < 0  or max(data['oldpeak']) > 7):
        logging.info('Loading Error: oldpeak OUT OF RANGE BOUNDS!!!')
        count= count+1

    # check binary variables
    elif (data['fbs'].any() !=0 and data['fbs'].any()  != 1):
        logging.info('Loading Error: fbs SHOULD BE BINARY VARIABLE!!!')
        count= count+1

    elif (data['sex'].any()  !=0 and data['sex'].any()  != 1):
        logging.info('Loading Error: sex SHOULD BE BINARY VARIABLE!!!')
        count= count+1

    elif (data['exang'].any()  !=0 and data['exang'].any()  != 1):
        logging.info('Loading Error: exang SHOULD BE BINARY VARIABLE!!!')
        count= count+1

    elif (data['target'].any()  != 0 and data['target'].any()  != 1):
        logging.info('Loading Error: target SHOULD BE BINARY VARIABLE!!!')
        count= count+1


    # check variables with 3 values
    elif (data['restecg'].any() !=0 and data['restecg'].any() != 1 and data['restecg'].any() !=2):
        logging.info('Loading Error: restecg OUT OF RANGE BOUNDS!!!')
        count= count+1

    elif (data['slope'].any() !=0 and data['slope'].any() != 1 and data['slope'].any() !=2):
        logging.info('Loading Error: slope OUT OF RANGE BOUNDS!!!')
        count= count+1

    # check variables with 4 values
    elif (data['cp'].any() !=0 and data['cp'].any() != 1 and data['cp'].any() !=2 and data['cp'].any() !=3):
        logging.info('Loading Error: cp OUT OF RANGE BOUNDS!!!')
        count= count+1
    elif (data['thal'].any() !=0 and data['thal'].any() != 1 and data['thal'].any() !=2 and data['thal'].any() !=3):
        logging.info('Loading Error: thal OUT OF RANGE BOUNDS!!!')
        count= count+1

    # check variables with 5 values
    elif (data['ca'].any() !=0 and data['ca'].any() != 1 and data['ca'].any() !=2 and data['ca'].any() !=3 and data['ca'].any() !=4):
        logging.info('Loading Error: ca OUT OF RANGE BOUNDS!!!')
        count= count+1

    logging.info('successfully loaded & validated data file')
    assert count == 0
