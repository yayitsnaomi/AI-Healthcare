import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

# DEBUG = True
# LOGGING_CONFIG = "logging/local.conf"
# PORT = 8000
# APP_NAME = "healthcare AI chatbot"
# HOST = "127.0.0.1"
# SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
# MAX_ROWS_SHOW = 100

# Project
PROJECT_ROOT_DIR = os.environ.get('PYTHONPATH')
CURRENT_SEASON = 2019

# S3
AWS_S3_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Logging
LOGGING_CONFIG_FILE = os.path.join(PROJECT_ROOT_DIR, 'config', 'logging', 'local.conf')

# SQL Alchemy
SQLALCHEMY_SQLITE_HOST = os.path.join(PROJECT_ROOT_DIR, 'data', 'mlb_database')

SQLALCHEMY_MYSQL_HOST = os.environ.get('MYSQL_HOST')
SQLALCHEMY_MYSQL_PORT = '3306'
SQLALCHEMY_MYSQL_USERNAME = os.environ.get('MYSQL_USER')
SQLALCHEMY_MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

SQLALCHEMY_HOST = SQLALCHEMY_SQLITE_HOST
SQLALCHEMY_TYPE = 'sqlite'  # Should be either 'sqlite' or 'mysql'
SQLALCHEMY_DATABASE_NAME = 'mlb'

import src.helpers.configHelpers as ch
SQLALCHEMY_DATABASE_URI = ch.createDatabaseURI(dbtype=SQLALCHEMY_TYPE,
    host=SQLALCHEMY_HOST, dbname=SQLALCHEMY_DATABASE_NAME,
    port=SQLALCHEMY_MYSQL_PORT, username=SQLALCHEMY_MYSQL_USERNAME,
    password=SQLALCHEMY_MYSQL_PASSWORD)