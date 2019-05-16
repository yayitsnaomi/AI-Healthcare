import os
import sys
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import yaml

sys.path.append('..')
import config
import argparse

#logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)
#logger = logging.getLogger('healthcarechatbot')

Base = declarative_base()

class Disease(Base):
    """ Defines the data model for the table `Disease`. """

    __tablename__ = 'Disease'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Source = Column(String(100), unique=False, nullable=False)
    Target = Column(String(100), unique=False, nullable=False)
    Weight = Column(Integer, unique=False, nullable=False)


    def __repr__(self):
        disease_data = "<Disease(id='%s', Source='%s', Target='%s', Weight='%s')>"
        return disease_data % (self.id, self.Source, self.Target, self.Weight)


class Heart(Base):
    """ Defines the data model for the table `Heart`."""

    __tablename__ = 'Heart'

    disease_id = Column(Integer, primary_key=True, unique=True, nullable=False)
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


    def __repr__(self):
        disease_data = "<Disease(disease_id='%s', age='%s',sex='%s' ,cp='%s' ,trestbps='%s' ,chol='%s' ,fbs='%s' ,restecg='%s' ,thalach='%s' ,exang='%s' ,oldpeak='%s' ,slope='%s' ,ca='%s' ,thal='%s' ,target='%s')>"
        return disease_data % (self.disease_id, self.age, self.sex, self.cp, self.trestbps, self.chol,self.fbs, self.restecg, self.thalach, self.exang, self.oldpeak,self.slope , self.ca, self.thal,self.target )


def _truncate_heart_data(session):
    """Deletes tweet scores table if rerunning and run into unique key error."""
    session.execute('''DELETE FROM Heart''')


def create_db(user,password,dbconfig):
    """Creates a database with the data models inherited from `Base` (Tweet and TweetScore).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if dbconfig is not None:
        with open(dbconfig, "r") as f:
            db = yaml.load(f)
    
        conn_type = db["type"]
        host = db["host"]
        port = db["port"]
        database = db["dbname"]
        user = user
        password = password
        engine_string = "{}://{}:{}@{}:{}/{}". \
            format(conn_type, user, password, host, port, database)
        try:

            engine = create_engine(engine_string)
            logger.info("Creating RDS database")
            #Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            logger.info("Database created with tables")
        except Exception as e:
            logger.error(e)
            sys.exit(1)

def create_connection(user,password,dbconfig):



    conn = create_engine(engine_string)

    return conn

def get_session(engine=None, engine_string=None):
    """

    Args:
        engine_string: SQLAlchemy connection string in the form of:

            "{sqltype}://{username}:{password}@{host}:{port}/{database}"

    Returns:
        SQLAlchemy session
    """

    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from tweet_scores table before create_all "
                             "so that table can be recreated without unique id issues ")
    parser.add_argument("--user", "-u",help="If given, delete current records from tweet_scores table before create_all "
                             "so that table can be recreated without unique id issues ")
    parser.add_argument("--password", "-p",help="If given, delete current records from tweet_scores table before create_all "
                             "so that table can be recreated without unique id issues ")
 
    args = parser.parse_args()

    # If "truncate" is given as an argument (i.e. python models.py --truncate), then empty the tweet_score table)
    if args.truncate:
        session = get_session(engine_string=config.SQLALCHEMY_DATABASE_URI)
        try:
            logger.info("Attempting to truncate heart table.")
            _truncate_tweet_score(session)
            session.commit()
            logger.info("Heart table truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate heart table.")
            logger.error(e)
        finally:
            session.close()

    create_db(args.user,args.password,config.DB_CONFIG)
