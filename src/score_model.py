#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: naomi
"""
import pandas as pd
import yaml
import pickle
import numpy as np
import sklearn
import argparse
from sklearn import model_selection
from sklearn import linear_model
import logging
import boto3
from io import StringIO
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from io import BytesIO

# add logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def gets3data(s3_bucket, s3_features):
    """[get data from s3]

    Arguments:
        s3_bucket {[str]} -- [pass in name of s3 bucket]
        s3_features {[str]} -- [pass in name of features to get data]

    Returns:
        [dataframe] -- [dataframe with values in csv file in s3 bucket]
    """

    client = boto3.client('s3')  # low-level functional API
    obj = client.get_object(Bucket=s3_bucket, Key=s3_features)
    numpyarray = np.load(BytesIO(obj['Body'].read()))
    return numpyarray

    # s3 = boto3.client('s3')
    # logging.info('Connecting to S3 bucket for data %s', s3_bucket)
    # obj = s3.get_object(Bucket=s3_bucket, Key=s3_features)
    # logging.info('Read file from s3 bucket %s', s3_features)
    #return pd.read_csv(obj['Body'])

def gets3model(s3_bucket, s3_model):
    """[getting pickle model from s3 bucket]

    Arguments:
        s3_bucket {[str]} -- [pass in name of s3 bucket]
        s3_model {[str]} -- [pass in name of path to model pickle file in s3 bucket]

    Returns:
        [pickle file] -- [model returned as pickle file]
    """
    #open the file
    logging.info('Connecting to S3 bucket for data %s', s3_bucket)

    s3 = boto3.resource('s3')
    with open(s3_model, 'wb') as data:
        s3.Bucket(s3_bucket).download_fileobj(s3_model, data)

    logging.info('Read file from s3 bucket %s', s3_model)

    with open(s3_model, 'rb') as data:
        return pickle.load(data)


def score_model(model, s3_bucket, x_test, y_test):
    """[evaluate the model and store output like the important images and files]

    Arguments:
        model {[pickle file]} -- [model stored as pickle file]
        s3_bucket {[str]} -- [name of s3 bucket passed in]
        x_test {[dataframe]} -- [data split into x features for testing]
        y_test {[dataframe]} -- [data split into y target vector for testing]
    """
    logging.info('Scoring model')

    # calculate cross validation scores for 5 fold & calculate mean accuracy rate
    scores = cross_val_score(model, x_test, y_test, cv=5)
    mean = scores.mean()

    #save scores and mean
    csv_buffer = StringIO()
    s3_resource = boto3.resource('s3')
    scores_df = pd.DataFrame({'CV score': scores})
    scores_df.to_csv(csv_buffer, index=False)
    s3_resource.Object(s3_bucket, 'results/CV_scores_5fold.csv').put(Body=csv_buffer.getvalue())
    #scores_df.Object(s3_bucket, 'results/CV_scores.csv').put(Body=csv_buffer.getvalue())


    csv_buffer2 = StringIO()
    mean_df = pd.DataFrame({'CV mean': mean}, index=[0])
    mean_df.to_csv(csv_buffer2, index=False)
    s3_resource.Object(s3_bucket, 'results/CV_mean.csv').put(Body=csv_buffer2.getvalue())
    #mean_df.Object(s3_bucket, 'CV_scores.csv').put(Body=csv_buffer2.getvalue())

    logging.info('Saving Cross Validation scores & mean score')
    # Creates a confusion matrix
    y_pred = model.predict(x_test)
    cm = confusion_matrix(y_test, y_pred)
    logging.info('Saving confusion matrix')

    # plot and save figure
    plt.figure(figsize=(5.5, 4))
    sns.heatmap(cm, annot=True)
    plt.title('Extra Trees Classifier \n Accuracy:{0:.3f}'.format(accuracy_score(y_test, y_pred)))
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('figures/confusion_matrix.png')
    logging.info('stored confusion matrix figure')

    # store image to s3
    logging.info('storing confusion matrix to s3')
    s3 = boto3.client('s3')
    file_name = 'figures/confusion_matrix.png'
    key_name = 'figures/confusion_matrix.png'
    s3.upload_file(file_name, s3_bucket, key_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="send in original data file ")
    parser.add_argument('--config', default="config/config.yml", help='path to yaml file with configurations')
    parser.add_argument('--input', default="data/features.csv", help='data of all features for the model')
    parser.add_argument('--input2', default="data/x_test.csv", help='path of the test data x features for model')
    parser.add_argument('--input3', default="data/y_test.csv", help='path fo the test data y target for the model')
    parser.add_argument('--input4', default="data/model.pkl", help='trained model file to test against')
    parser.add_argument('--output', default="data/CV_scores.csv", help='5 fold cross validation scores')
    parser.add_argument('--output1', default="data/CV_mean.csv", help='mean value of cross validation output')
    parser.add_argument('--output3', default="data/confusion_matrix.png", help='confusion matrix plot as png')

    args = parser.parse_args()

    # import yaml config
    with open(args.config, "r") as f:
        config = yaml.load(f)

    logging.info('In score_model.py')

    # get model pickle file
    model = gets3model(config["score_model"]["s3_bucket"],config["score_model"]["s3_model"])

    # get s3 data
    bucket = config["score_model"]["s3_bucket"]
    x_test = gets3data(bucket, config["score_model"]["s3_x_test"] )
    y_test = gets3data(bucket, config["score_model"]["s3_y_test"] )

    # score model
    score_model(model, bucket, x_test, y_test)

    logging.info('Saved evaluation output')