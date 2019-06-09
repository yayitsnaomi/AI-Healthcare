import os
import sys
import pickle
#import traceback
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for
import logging
#from app import db, app
from flask import Flask
#sys.path.insert(0, 'src/')
from flask_sqlalchemy import SQLAlchemy
import sklearn
sys.path.append(os.path.join('..'))
from src.score_model import gets3model
import boto3

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_object('config')

# configure logging
logging.basicConfig(filename='heart_doc_flask.log', level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index(): # connecting the app , flask syntax
    """Homepage of this prediction system.

    Returns: rendered html template
    """
    #return render_template('index_heart.html')

    try:
        logger.info("Rendering home page")
        return render_template('index_heart.html')
    except:
        logger.warning("Not able to display homepage, error page returned")
        return render_template('error.html') # error if index not found

@app.route('/add', methods=['POST','GET'])
def add_entry():
    """View that process a POST with new customer input
    Returns: rendered html template with evaluation results.
    """
    # retrieve features
    try:
        logger.info("start retrieving features from UI!")

        age = request.form['age']
        sex = request.form['sex']
        cp = request.form['cp']
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach = request.form['thalach']
        exang = request.form['exang']
        oldpeak = request.form['oldpeak']
        slope = request.form['slope']
        ca = request.form['ca']
        thal = request.form['thal']
        logger.info("all inputs retrieved!")

        # load trained model form s3
        logger.info("loading model from s3!")

        session = boto3.session.Session(region_name='eu-west-1')
        s3client = session.client('s3')
        response = s3client.get_object(Bucket=app.config["S3BUCKET"], Key='data/model.pkl')
        body = response['Body'].read()
        model = pickle.loads(body)

        # predicting heart disease with user input
        predicted = model.predict(pd.DataFrame({'age': age,
                                                'sex': sex,
                                                'cp': cp,
                                                'trestbps': trestbps,
                                                'chol': chol,
                                                'fbs': fbs,
                                                'restecg': restecg,
                                                'thalach': thalach,
                                                'exang': exang,
                                                'oldpeak': oldpeak,
                                                'slope': slope,
                                                'ca': ca,
                                                'thal': thal
                                                }, index=[0]))

        # translate output into readable prediction for UI
        if(predicted ==0):
            result = "Patient is not at risk for heart disease"
        else:
            result = "Patient is at risk of having heart disease"

        # render input page with updated result
        return render_template('index_heart.html', result=result)
    except:
        logger.warning("Not able to display homepage, error page returned")
        return render_template('error.html') # error if index not found

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
