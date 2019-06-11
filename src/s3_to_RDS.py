"""
@author: naomi
"""
import os
import sys
import logging
import logging.config
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import yaml
import pymysql
import argparse


# add logging 
logging.basicConfig(filename='heart_doc.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# declare base
Base = declarative_base()

class Heart(Base):
    """ Defines the data model for the table `Heart` with columns required to run model pipeline"""

    __tablename__ = 'Heart'

    # columns required for features (except ID)
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    age = Column(Integer, unique=False, nullable=False)
    sex = Column(Integer, unique=False, nullable=False)
    cp = Column(Integer, unique=False, nullable=False)
    trestbps = Column(Integer, unique=False, nullable=False)
    chol = Column(Integer, unique=False, nullable=False)
    fbs = Column(Integer, unique=False, nullable=False)
    restecg = Column(Integer, unique=False, nullable=False)
    thalach = Column(Integer, unique=False, nullable=False)
    exang = Column(Integer, unique=False, nullable=False)
    oldpeak = Column(Float, unique=False, nullable=False)
    slope = Column(Integer, unique=False, nullable=False)
    ca = Column(Integer, unique=False, nullable=False)
    thal = Column(Integer, unique=False, nullable=False)
    target = Column(Integer, unique=False, nullable=False)

    logger.info("Defining data model Heart")

    def __repr__(self):
        patient_data = "<Heart(id='%s', age='%s',sex='%s' ,cp='%s' ,trestbps='%s' ,chol='%s' ,fbs='%s' ,restecg='%s' ,thalach='%s' ,exang='%s' ,oldpeak='%s' ,slope='%s' ,ca='%s' ,thal='%s' ,target='%s')>"
        return patient_data % (self.id, self.age, self.sex, self.cp, self.trestbps, self.chol,self.fbs, self.restecg, self.thalach, self.exang, self.oldpeak,self.slope , self.ca, self.thal,self.target )


def _truncate_heart_data(session):
     """Deletes table, called each time this file is run so data is not accidently appended"""
     session.execute('''DELETE FROM Heart''')
     logger.info("truncating Heart table")


def create_db(user,password,database, conn_type, host, port):
    """Creates a database with the data models inherited from `Base`

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    logger.info("Creating RDS database")

    # create engine string with details from yaml file
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(conn_type, user, password, host, port, database)

    engine = create_engine(engine_string)
    Base.metadata.create_all(engine)
    logger.info("Database created with tables")
    return engine


def create_connection(user,password,dbconfig):
    logger.info("creating RDS connection")
    conn = create_engine(engine_string)
    return conn

def get_session(engine=None, engine_string=None):
    """gets session and calls create connection to RDS
    Args:
        engine_string: SQLAlchemy connection string in the form of:

            "{sqltype}://{username}:{password}@{host}:{port}/{database}"

    Returns:
        SQLAlchemy session
    """

    # error checking that engine string was passed into function 
    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument('--config', default="../config/config.yml", help="config yaml file with parameters")
    parser.add_argument("--user", "-u",help="pass in user name credential for DB ")
    parser.add_argument("--password", "-p",help="pass in password credential for DB")
    args = parser.parse_args()
    logger.info("Loading data from s3 to RDS")

    # import yaml config
    with open(args.config, "r") as f:
        config = yaml.load(f)


    # create DB
    engine= create_db(args.user, args.password, config["ingest_data"]["db_name"], config["ingest_data"]["conn_type"], config["ingest_data"]["host"], config["ingest_data"]["port"])
    logger.info("created db")

    # connect to s3 with bucket and file path
    s3_data = pd.read_csv(config["ingest_data"]["s3_path"])
    # get engine
    session = get_session(engine)

    # truncate table
    logger.info("Truncate existing RDS database table Heart")
    _truncate_heart_data(session)

    # insert
    logger.info("Insert data from s3 into RDS database")
    session.bulk_insert_mappings(Heart, s3_data.to_dict(orient="records")) # take from s3 and put into heart
    session.commit()

