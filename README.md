
# ChatBot
## Project Charter

**Vision**: Provide individuals across the world with access to affordable, quality healthcare. Doctors are limited and AI applications in healthcare are advancing to enable quality care via internet access.

**Mission**: As individuals are moving towards personalized Healthcare, we can leverage the power of AI chatbots to comfort patients and provide a first pass diagnosis based on symptoms, along with a confidence threshold of the predicted diagnosis. Goal is to enable users to get a diagnosis for their current symptoms. The hopes would be that people get a better diagnosis than what they would from googling symptoms themselves. Users can also chat with Eliza the therapy bot, when they feel like they need someone to listen to them; which has proven to be calming.

**Success criteria**: 
-  **Machine Learning Performance**: 
	- Misclassification Rate - number of correctly diagnosed diseased based on the symptom. 
	- Acceptance Criteria: Misclass rate < 0.3, meaning 70% of test data in cross validation is accurately diagnosed.
- **Business Outcome**: 
	- number of users that use this app instead of googling their symptoms. 
	- number of exchanges with the therapy bot, and improved user mood based on pre conversation and post conversation.

## Backlog

**Sprint Sizing Legend:**
 - 0 points - quick chore 
 - 1 point ~ 1 hour (small) 
 - 2 points ~ 1/2 day (medium) 
 - 4 points ~ 1 day (large) 
 - 8 points - big and needs to be broken down more when it comes to execution (okay as placeholder for future work though)

-   **Design --**
    -   **Chatbot**: Research and leverage Chatbot API for natural language processing (2 pts)
    -   **Architecture**: Design architecture and end to end data flow (2pts)
    -   **UI Wireframe**: Design UI front end: Chatbot interface with user (4pts)
    -   **Data**: Create Training / Test Data files: symptoms and diagnosis (4pts)
-   **Develop --**
    -   **Environment setup**:
        -   Set up virtual environment: ec2 (4pts)
        -   Create requirements.txt (1pt)
    -   **Model**:
        -   Build Decision Tree: Classification of disease model (4pts)
        -   Build model accuracy metrics (i.e. misclassification rate) (4pts)
        -   Build model prediction confidence interval (2pts)
    -   **UI**:
        -   Build chatbot interaction with user inputs & model output (8pts)
    -   **Scripts**:
        -   Create script to run training file on model (4pts)
        -   Create script to call prediction function with user input (4pts)
-   **Test --**
    -   **Unit**  Test Scripts: for code (4pts)
    -   **UAT**  Test Scripts: for UI (4pts)
-   **Deploy --**  Push the final version to Github and double check UAT test cases (4pts)

**Backlog : Icebox --**  
- Recommend doctor for each diagnosis based on closest via patient address

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
