import boto3
import sys
import os

sys.path.append('..')
import config
#import S3_Bucket_name

s3 = boto3.client('s3')

s3.download_file('healthcarechatbot','data/dataset_clean.csv','dataset_clean.csv')
s3.download_file('healthcarechatbot','data/heart.csv','heart.csv')

s3.upload_file('dataset_clean.csv',config.S3_Bucket_name,'dataset_clean_reuploaded_from_script.csv')
s3.upload_file('heart.csv',config.S3_Bucket_name,'heart_reuploaded_from_script.csv')
