"""
@author: naomi
"""
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
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

def getRDSdata(conn):
    """[get original heart disease kaggle data from RDS to feed into pipeline]

    Arguments:
        conn {[pymysql connection]} -- [connection details to connect to RDS]

    Returns:
        [dataframe] -- [dataframe with the full data set for heart disease]
    """
    # EXCEPTION HANDLING: quit if loading data is not able to run
    try: 
        logging.info('Selecting data from RDS and bringing it into pipeline as pandas df')
        pandas_df=pd.read_sql('select * From Heart', con=conn)
        return pandas_df
    except:
        logger.warning("Not able to connect to RDS to load data")
        sys.exit(1)

def feature_correlation(s3_bucket, data):
    """[calculate feature cross correlation matrix]

    Arguments:
        data {[dataframe]} -- [all features to plot in cross correlation matrix]
    """
    # EXCEPTION HANDLING: warning if figure is not able to plot
    try:
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
        # plot and save
        figure = corrPlot.get_figure()
        figure.savefig('figures/features_correlation_heatmap.png')

        # store image to s3
        logging.info('storing confusion matrix to s3')
        s3 = boto3.client('s3')
        file_name = 'figures/features_correlation_heatmap.png'
        key_name = 'figures/features_correlation_heatmap.png'
        s3.upload_file(file_name, s3_bucket, key_name)
        logging.info('stored correlation heapmap figure')
    except:
        logger.warning("Not able to save correlation matrix figure")


def save_data(data, s3_bucket, s3_clean):
    """[save data to s3 bucket]

    Arguments:
        data {[dataframe]} -- [send in data]
        s3_bucket {[string]} -- [name of s3 bucket]
        s3_clean {[string]} -- [path to clean data file]
    """
    # EXCEPTION HANDLING: quit if not able to save data b/c next steps will fail
    try:
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(s3_bucket, s3_clean).put(Body=csv_buffer.getvalue())
        logging.info('wrote clean data to s3 bucket to file %s', s3_clean)
    except:
        logger.warning("Not able to save clean data to s3")
        sys.exit(1)


if __name__ == "__main__":
    """[This main function is responsible for loading data from s3 bucket ]
    """
    # get arguments from parser
    parser = argparse.ArgumentParser(description="send in original data file ")
    parser.add_argument('--config', default="config/config.yml", help='path to yaml file with configurations')
    parser.add_argument('--input', default="data/heart.csv", help='send in the heart data from kaggle')
    parser.add_argument('--output', default="data/heart_clean.csv", help='store the data in database')
    parser.add_argument("--user", "-u",help="pass in user name credential for RDS ")
    parser.add_argument("--password", "-p",help="pass in password credential for RDS")
    args = parser.parse_args()

    # pull specified configurations from YAML file
    with open(args.config, "r") as f:
        config = yaml.load(f)

    logging.info('Executing load_data.py to get data and validate it before creating features')

    # connect to RDS
    conn = pymysql.connect(host=config["load_data"]["host"], user=args.user, port=config["load_data"]["port"], passwd=args.password, db=config["load_data"]["db_name"])

    # get RDS data into pipline
    data = getRDSdata(conn)
    logging.info('Created RDS connection')

    #calculate cross correlation between all features to determine if any are able to be dropped
    bucket = config["load_data"]["s3_bucket"]
    logging.info('Calculating feature correlation')
    feature_correlation(bucket, data)

    # write data to CSV
    clean_path = config["load_data"]["s3_clean"]
    save_data(data, bucket, clean_path )
    logging.info('Successfully saving validated patient heart disease feature data')


