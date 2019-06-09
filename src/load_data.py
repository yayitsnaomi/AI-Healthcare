from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import numpy as np
import yaml
import logging
import math
import boto3
import sys
import os
from io import StringIO
import pymysql

# set up logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# def gets3data(s3_bucket, s3_raw):
#     """[get data from s3 bucket]

#     Arguments:
#         s3_bucket {[string]} -- [name of the s3 bucket from config.yml]
#         s3_raw {[string]} -- [name of the s3 raw data file path config.yml]

#     Returns:
#         [dataframe] -- [returns the data as a dataframe]
#     """

#     # import S3_Bucket_name
#     s3 = boto3.client('s3')
#     logging.info('Connecting to S3 bucket for data %s', s3_bucket)
#     obj = s3.get_object(Bucket=s3_bucket, Key=s3_raw)
#     logging.info('Read file from s3 bucket %s', s3_raw)
#     return pd.read_csv(obj['Body']) # return as df

def getRDSdata(conn): 

    pandas_df=pd.read_sql('select * From Heart', con=conn)
    return pandas_df

def feature_correlation(s3_bucket, data):
    """[calculate feature cross correlation matrix]

    Arguments:
        data {[dataframe]} -- [all features to plot in cross correlation matrix]
    """
    # Compute the correlation matrix
    corr = data.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    corrPlot = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                           square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)

    figure = corrPlot.get_figure()
    figure.savefig('figures/features_correlation_heatmap.png')

    # store image to s3
    logging.info('storing confusion matrix to s3')
    s3 = boto3.client('s3')
    file_name = 'figures/features_correlation_heatmap.png'
    key_name = 'figures/features_correlation_heatmap.png'
    s3.upload_file(file_name, s3_bucket, key_name)

    #my_bucket.upload_file(figure, Key='features_correlation_heatmap.png')
    logging.info('stored correlation heapmap figure')


def save_data(data, s3_bucket, s3_clean):
    """[save data to s3 bucket]

    Arguments:
        data {[dataframe]} -- [send in data]
        s3_bucket {[string]} -- [name of s3 bucket]
        s3_clean {[string]} -- [path to clean data file]
    """
    csv_buffer = StringIO()
    data.to_csv(csv_buffer, index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(s3_bucket, s3_clean).put(Body=csv_buffer.getvalue())

    #my_bucket.upload_fileobj(data, Key=s3_clean)
    logging.info('wrote validated feature data to s3 bucket to file %s', s3_clean)


if __name__ == "__main__":
    """[This main function is responsible for loading data from s3 bucket ]
    """
    # get arguments from parser
    parser = argparse.ArgumentParser(description="send in original data file ")
    parser.add_argument('--config', default="config/config.yml", help='path to yaml file with configurations')
    parser.add_argument('--input', default="data/heart.csv", help='send in the heart data from kaggle')
    parser.add_argument('--output', default="data/heart_clean.csv", help='store the data in database')
    parser.add_argument("--user", "-u",help="pass in user name credential for DB ")
    parser.add_argument("--password", "-p",help="pass in password credential for DB")
    args = parser.parse_args()

    # pull specified configurations from YAML file
    with open(args.config, "r") as f:
        config = yaml.load(f)

    logging.info('Executing load_data.py to get data and validate it before creating features')

    # parse attributes for reading data
    #data = gets3data(config["load_data"]["s3_bucket"], config["load_data"]["s3_raw"])
    # connect to RDS
    
    conn = pymysql.connect(host=config["load_data"]["host"], user=args.user, port=config["load_data"]["port"], passwd=args.password, db=config["load_data"]["db_name"])

    # get RDS data into pipline
    data = getRDSdata(conn)

    #calculate cross correlation between all features to determine if any are able to be dropped
    bucket = config["load_data"]["s3_bucket"]
    feature_correlation(bucket, data)

    # write data to CSV
    clean_path = config["load_data"]["s3_clean"]
    save_data(data, bucket, clean_path )
    logging.info('Successfully saving validated patient heart disease feature data')


