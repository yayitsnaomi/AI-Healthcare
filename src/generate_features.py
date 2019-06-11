#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: naomi
"""
import numpy as np
import yaml
import argparse
import pandas as pd
import logging
import boto3
import sys
from io import StringIO

# set up logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def gets3data(s3_bucket, s3_clean):
    """[get data from s3 bucket]

    Arguments:
        s3_bucket {[string]} -- [name of the s3 bucket from config.yml]
        s3_raw {[string]} -- [name of the s3 raw data file path config.yml]

    Returns:
        [dataframe] -- [returns the data as a dataframe]
    """
    try:
        # import S3_Bucket_name
        s3 = boto3.client('s3')
        logging.info('Connecting to S3 bucket for data %s', s3_bucket)
        obj = s3.get_object(Bucket=s3_bucket, Key=s3_clean)
        logging.info('Read file from s3 bucket %s', s3_clean)
        return pd.read_csv(obj['Body'])
    except:
        logger.warning("Not able to get data from s3")
        sys.exit(1)


def generate_features(data):
    """ This function generates additional calculated features required by the model

        :param df:  send in the dataframe of features
        :param target:  send in the target data
        :param columns: send in the columns of attributes in the data
    """
    try:
        logging.info('Generating features')
        # drop variables no needed
        heart_data = data.drop('oldpeak', axis=1)
        # create dummy variables for categorical variables
        heart_data_factored = pd.get_dummies(data=heart_data, columns=['restecg', 'cp', 'slope', 'ca', 'thal'])
        logging.info('Generated features successfully')
        return heart_data_factored
    except:
        logger.warning("Not able to generate features & factor dummies")
        sys.exit(1)


def save_data(features, s3_bucket, s3_features):
    """[save data to s3 bucket]

    Arguments:
        data {[dataframe]} -- [send in data]
        s3_bucket {[string]} -- [name of s3 bucket]
        s3_features {[string]} -- [path to features data file]
    """
    try:
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(s3_bucket, s3_features).put(Body=csv_buffer.getvalue())
        #my_bucket.upload_fileobj(data, Key=s3_clean)
        logging.info('wrote validated feature data to s3 bucket to file %s', s3_features)
    except:
        logger.warning("Not able to save feature data to s3")
        sys.exit(1)

if __name__ == "__main__":
    # get arguments from parser

    logging.info('In generate feature')

    parser = argparse.ArgumentParser(description="send in original data file ")
    parser.add_argument('--config', default="config/config.yml", help='path to yaml file with configurations')
    parser.add_argument('--input', default="data/heart_clean.csv", help='path to clean data file')
    parser.add_argument('--output', default="data/features.csv", help='path to save dataframe features')
    args = parser.parse_args()

    # pull specified configurations from YAML file
    with open(args.config, "r") as f:
        config = yaml.load(f)

    # get data from s3
    clean_path = config['generate_features']['s3_clean']
    bucket = config['generate_features']['s3_bucket']
    data = gets3data(bucket, clean_path)

    # call features to generate features and store output
    features = generate_features(data)

    # save features
    save_data(features, bucket,  config["generate_features"]["s3_features"])


