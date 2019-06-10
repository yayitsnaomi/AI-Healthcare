import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 9020
APP_NAME = "AI_healthcare"
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "127.0.0.1"
MAX_ROWS_SHOW = 15
S3BUCKET = 'healthcarechatbot'
S3_MODEL_PATH: 's3://healthcarechatbot/data/model.pkl'
model_path = 'model.pkl'