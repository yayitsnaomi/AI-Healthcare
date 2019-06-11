
# Digital Doctor (Cardiologist): 
"Healthcare at your fingertips"

Link for app hosted on EC2: http://35.161.103.249:3000

![alt text](https://github.com/yayitsnaomi/Chatbot-AI-Healthcare/blob/master/img/cardiologist.png)


**AI Cardiologist: Heart Disease Data Source Credit:**
https://www.kaggle.com/ronitf/heart-disease-uci
Data consists of 14 key attributes of patient health to predict level of heart disease.
 
# Steps to run python scripts & parts of analytic pipeline 
**Note: This is used for running locally or on MSIA server - data landed in RDS & pipeline output stored to S3**

**1. SSH into MSiA Server**
 - ssh nak133@msia423.analytics.northwestern.edu

**2. Create new environment**
 - conda create --name test_env python=3.7
 - conda activate test_env

**3. Clone the git project into the env:  test_env**
 - git init
 - git clone https://github.com/yayitsnaomi/AI-Healthcare.git

**4. Go into AI-Healthcare/ folder**
 - cd AI-Healthcare/

**5. Install requirements.txt file**
 - pip install -r requirements.txt

**6. Update AWS Configuration: configure AWS settings with your username and pass credentials**
	aws configure
	- enter your secret key id
	- and secret key password
	- pros enter for default region name
	- press enter for default output format

**7. Update config file as required for RDS connection: PORT, HOST. This is also where s3 paths can be updated.**
	- cd config
	- vi config.yml
	- Edit Ingest_data parameters as required to test RDS connection:
		- db_Name
		- conn_type
		- host
		- post

**7a. Go into SRC folder**
 - cd .. 
 - cd src/

**8. Run s3_to_RDS and feed in your username (root) and password to connect to RDS**
 - python s3_to_RDS.py --user root --password <password>

**9. Come back to main folder**
 - cd ..

**10. Run load_data, again feed in your username (root) and password**
 - python src/load_data.py --user root --password <password>

**11. Run pipeline from generate features -> score model**
 - make all

**12. Go into app and run the app to launch**
 - cd app
 - python app.py

**13. View app(unless configured otherwise) at:** http://127.0.0.1:9020/ 

# Steps deploy the app on EC2:

**1. SSH onto EC2 Instance**

**2. Create new environment**
 - conda create --name test_env python=3.7
 - conda activate test_env

**3. Clone the git project into the env:  test_env**
 - git init
 - git clone https://github.com/yayitsnaomi/AI-Healthcare.git

**4. Go into AI-Healthcare/ folder**
 - cd AI-Healthcare/

**5. Install requirements.txt file**
 - pip install -r requirements.txt

**6. Change the HOST from "127.0.0.1" to "0.0.0.0" of config in app folder, file: config.py. 
   Also change the PORT from 9020 to 3000. 
   Save the file.**
 - vi app/config.py

**7. Check screen version**
 - screen --version

**8. Start screen named session**
 - screen -S msia423-screen-session
 - conda activate test_env

**9. Run app**
 - python app.py


## Project Charter

**Vision**: Provide individuals across the world with access to affordable, quality healthcare. Doctors are limited and AI applications in healthcare are advancing to enable quality care via AIs and internet access.

**Mission**: As individuals are moving towards personalized Healthcare, we can leverage the power of AI chatbots to comfort patients and provide a first pass diagnosis based on symptoms. ~ 2,300 Americans die of cardiovascular disease each day, average of 1 death every 38 seconds. Direct and indirect costs of total cardiovascular diseases and stroke are estimated to total more than $329.7 billion* includes health expenditures & lost productivity. [Citation: American Heart Association]
 
**Success criteria**:

-   **Machine Learning Performance**:
    -   Misclassification Rate - number of correctly diagnosed based on the patient history.
    -   Confusion Matrix - Low false postiives are also important to track for healthcare outcomes.
    -   Acceptance Criteria: Misclass < 20% i.e. accuracy > 80%. 
-   **Business Outcome**:
    -   Number of users that use this app instead of googling their symptoms.
    -   Number of stars users rate the app

## Planning

### Theme 1: Create an AI doctor that can suggest the most likely disease based on your list of symptoms. --> [DROPPED DUE TO LACK OF GOOD DATA]

-   **Epic 1:** Create an analytic that can suggest the most likely diagnosis based on user specified symptoms, along with a confidence interval
	-   **US0:** Environment setup: install any required packages, libraries. Spin up EC2 on AWS. Create requirements.txt to make reproducible environment. 
    -   **US1:** Find a good data set for training, including: list of symptoms, disease, and the count of disease occurrence. 
    -   **US2:** Complete data transformations in python so the data can be fed into the model
    -   **US3:** Create a AWS RDS to store user input from UI and model output
    -   **US4:** Build decision tree based classification model in python
    -   **US5:** Complete cross validation measuring misclassification rate & tune decision tree parameters until reaching an optimal threshold 
    -   **US6:** Build confidence interval into the model output 
    -   **US7:** Create unit test scripts to test all model functionality is working as expected
    -   **US8:** Create a CSS/HTML UI with drop down fields so users can select from a predefined list of symptoms that the model has been trained on
    -   **US9:** Create script that takes the user input from UI and flask wrapper that feeds it into the decision tree model predict function to get an output
    -   **US10:** Create functionality to display the predicted disease outputted and Confidence interval from the model onto the UI
    -   **US11**  Create UAT test scripts to test that UI is working as expected to intake selections and output accordingly
    -    **US12:** Create logging for easy debugging and error notifications
    -    **US13:** Deploy into Production environment and double check UAT test cases

### Theme 2: Create an AI doctor that can diagnose heart disease based on patient health factors
-   **Epic 2:** Create an analytic that can suggest the most likely to diagnose heart disease based on patient health factors
    -   **US14:** Environment setup: install any required packages, libraries. Spin up EC2 on AWS. Create requirements.txt to make reproducible environment.
    -   **US15:** Find a good data set for training, including: list of features of heart disease
    -   **US16:** Build extra trees classifier ensamble classification model in python
    -   **US17:** Build UI of cardiologist doctor and form to accept inputs

## Backlog

**Sprint Sizing Legend:**
-   0 points - quick chore
-   1 point ~ 1 hour (small)
-   2 points ~ 1/2 day (medium)
-   4 points ~ 1 day (large)
-   8 points - big and needs to be broken down more when it comes to execution (okay as placeholder for future work though)
    

14. **Theme2.epic1.story1**  (2pts) - COMPLETED: sprint 1
15. **Theme2.epic1.story2**  (2pts) - COMPLETED: sprint 1
16. **Theme2.epic1.story3**  (4pts) - COMPLETED: sprint 1
17. **Theme2.epic1.story4**  (2pts) - COMPLETED: sprint 1



## Icebox

-   **Theme3**: Recommend doctor for each diagnosis based on closest via patient address

## Repo Structure

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```

