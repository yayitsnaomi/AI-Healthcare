#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: naomi
"""
import pandas as pd
import argparse
import yaml
import pickle
from sklearn import model_selection
from sklearn import linear_model
import logging
import boto3
from io import StringIO
import io
import numpy as np
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt

# set up logging
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def gets3data(s3_bucket, s3_features):
    """[get data from s3 bucket]

    Arguments:
        s3_bucket {[string]} -- [name of the s3 bucket from config.yml]
        s3_features {[string]} -- [name of the s3 features path from config.yml]

    Returns:
        [dataframe] -- [returns the data as a dataframe]
    """
    s3 = boto3.client('s3')
    logging.info('Connecting to S3 bucket for data %s', s3_bucket)
    obj = s3.get_object(Bucket=s3_bucket, Key=s3_features)
    logging.info('Read file from s3 bucket %s', s3_features)
    return pd.read_csv(obj['Body'])



def build_model(s3_bucket, features, size):
    """ function builds the training model on train data
        :param features: send in model features data
        :param target:  send in model target data
        :param size:  send in the size to use for training/testing split (30% default to test)
        :param model_features:  send in the final features to run the model on
        Returns: the model and the test sets for x and y
    """

    features = features.drop('disease_id', 1)
    y = features[['target']]  # final column in target column (binary 1 or 0 for heart disease)
    x = features.drop('target', 1)

    # cross validation
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=size, random_state=42)
    print(x_train)
    print("y_train")
    print(y_train)
    # extra trees classifier- Build a forest and compute the feature importances
    forest = ExtraTreesClassifier(n_estimators=250,
                                  random_state=0)

    extraTreesModel = forest.fit(x_train, y_train)
    #print("Accuracy on split test: ", forest.score(x_test, y_test))

    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)

    # Plot the feature importance of the forest
    plt.figure()
    plt.title("Feature Importance")
    plt.barh(range(x_train.shape[1]), importances[indices],
             color="pink", align="center")  
    plt.yticks(range(x_train.shape[1]), x_train.columns)
    plt.ylim([-1, x_train.shape[1]])
    plt.savefig('figures/feature_importance_bar_chart.png')

    # store image to s3
    logging.info('stored feature importance from model bar plot')
    s3 = boto3.client('s3')
    file_name = 'figures/feature_importance_bar_chart.png'
    key_name = 'figures/feature_importance_bar_chart.png'
    s3.upload_file(file_name, s3_bucket, key_name)


    return extraTreesModel, x_test, y_test


def save_model(model, s3_bucket, s3_model, x_test, y_test, x_test_path, y_test_path):
    """ Saves the model and test sets for x and y at specified file paths
        :param model: model to store in pickle file
        :param model_path: path to store the model
        :param X_test:  data of x testing features
        :param y_test:  data of y testing target
    """
    logging.info('Saving model')
    #pickle.dump(model, open('models/model.pkl', 'wb'))

    #save model
    s3_resource = boto3.resource('s3')
    pickle.dump(model, open(s3_model, "wb"))
    s3_resource.Object(s3_bucket, s3_model).put(Body=open(s3_model, 'rb'))

    # save numpy x test to s3
    s3_resource = boto3.resource('s3')
    np.save(open(x_test_path, "wb"), x_test)
    s3_resource.Object(s3_bucket, x_test_path).put(Body=open(x_test_path, 'rb'))

    # save numpy y test to s3
    s3_resource = boto3.resource('s3')
    np.save(open(y_test_path, "wb"), y_test)
    s3_resource.Object(s3_bucket, y_test_path).put(Body=open(y_test_path, 'rb'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="send in original data file ")
    parser.add_argument('--config', default="config/config.yml", help='path to yaml file with configurations')
    parser.add_argument('--input', default="data/heart_features.csv", help='data of all features for the model')
    parser.add_argument('--output1', default="data/model.pkl",
                        help='model')
    parser.add_argument('--output2', default="data/x_test.csv",
                        help='path of the output test data x features for model')
    parser.add_argument('--output3', default="data/y_test.csv",
                        help='path of the output test data y target for the model')
    args = parser.parse_args()

    # pull specified configurations from YAML file
    with open(args.config, "r") as f:
        config = yaml.load(f)

    logging.info('In train_model.py')

    # load data from s3
    data = gets3data(config["train_model"]["s3_bucket"], config["train_model"]["s3_features"])

    # build model & review feature importance
    model, x_test, y_test = build_model(config["train_model"]["s3_bucket"], data, config["train_model"]["test_size"])

    # save model
    save_model(model, config["train_model"]["s3_bucket"], config["train_model"]["s3_model"], x_test, y_test, config["train_model"]["s3_x_test"], config["train_model"]["s3_y_test"])

    logging.info('Saved model output and train test sets')