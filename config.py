from os import path

# configure for s3
S3_Bucket_name = 'avcprivatebucket'

#configure for DB connection to local SQlite

# host = db["host"]
# database = ifin("dbname", db, "")
# sqltype = ifin("type", db, sqltype)
# port = db["port"]
# user_env = db["user_env"]
# password_env = db["password_env"]

# # Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.abspath(__file__))
DB_CONFIG = path.join(PROJECT_HOME,'config/db_config.yml')

# # App config
# APP_NAME = "sportco"
# DEBUG = True

# # Logging
#LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# # Database connection config
DATABASE_PATH = path.join(PROJECT_HOME, 'data/chatbot.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////{}'.format(DATABASE_PATH)
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# # API configs
# HOST = "127.0.0.1"
# PORT = 10000
# API_SENTIMENT_PATH='sentiment'
# API_ENDPOINT="http://{}:{}/{}".format(HOST, PORT, API_SENTIMENT_PATH)

# # Acquire and process config
# MAX_RECORDS_READ = 100
# SENTIMENT_RAW_LOCATION = path.join(PROJECT_HOME,'data/tweet_sentiment.json')