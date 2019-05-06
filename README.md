
# Healthcare AI Chatbot

Link: https://yayitsnaomi.github.io/Chatbot-AI-Healthcare/

Disease Symptom Data Source Credit: http://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html

![alt text](https://github.com/yayitsnaomi/Chatbot-AI-Healthcare/blob/master/figures/Chatbot_UI_6_6_2019.png)

## Project Charter

**Vision**: Provide individuals across the world with access to affordable, quality healthcare. Doctors are limited and AI applications in healthcare are advancing to enable quality care via AIs and internet access.

**Mission**: As individuals are moving towards personalized Healthcare, we can leverage the power of AI chatbots to comfort patients and provide a first pass diagnosis based on symptoms, along with a confidence threshold of the predicted diagnosis. Goal is to enable users to get a diagnosis for their current symptoms. The hopes would be that people get a better diagnosis than what they would from googling symptoms themselves. Users can also chat with Eliza the therapy bot, when they feel like they need someone to listen to them; which has proven to be calming.

**Success criteria**:

-   **Machine Learning Performance**:
    -   Misclassification Rate - number of correctly diagnosed diseased based on the symptom.
    -   Acceptance Criteria: Misclass rate < 0.5, meaning 50% of test data in cross validation is accurately diagnosed. 50% is acceptable in this case because there are so many diseases, with overlapping symptoms, that classificaiton might be challenging to get a very low miscass rate. If this proves to be the case, might explore providing the top 3 diagnoses and seeing if the correct diagnosis is indeed in the top 3.
-   **Business Outcome**:
    -   Number of users that use this app instead of googling their symptoms.
    -   Number of exchanges with the therapy bot, and improved user mood based on pre conversation and post conversation.
    -   Number of stars users rate the app

## Planning

### Theme 1: Create an AI doctor that can suggest the most likely disease based on your list of symptoms. 

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
    
### Theme 2: Create an AI therapist. It has been found to be calming and this would be helpful as users might be distressed as they are receiving their diagnoses. 

-   **Epic 2:**  Integrate with ELIZA therapy chat-bot with sentiment detection and response via avatars so that there is a comforting AI to listen to users, without judgement. 
    -   **US1:** Integrate ELIZA Javascript codes: Elizabot.js, elizadata.js, setimood.js 
    -   **US2:** Integrate ELIZA images for avatar: happy, sad, excited, etc
    -   **US3:** Create custom HTML/CSS file to visualize Eliza therapy bot chat next to the symptom diagnoser
    -   **US4:** UAT test scripts to test ELIZA is properly integrated into the UI and all functionality is working as expected

## Backlog

**Sprint Sizing Legend:**
-   0 points - quick chore
-   1 point ~ 1 hour (small)
-   2 points ~ 1/2 day (medium)
-   4 points ~ 1 day (large)
-   8 points - big and needs to be broken down more when it comes to execution (okay as placeholder for future work though)
    
    
0.  **Theme1.epic1.story0** (2pts) - PLANNED: sprint 1
1.  **Theme1.epic1.story1** (2pts) - PLANNED: sprint 1
2.  **Theme1.epic1.story2** (1pts) - PLANNED: sprint 1
3.  **Theme1.epic1.story3** (2pts) - PLANNED: sprint 1
4.  **Theme1.epic1.story4** (4pts) - PLANNED: sprint 1
5.  **Theme1.epic1.story5** (2pts)
6.  **Theme1.epic1.story6** (1pts)
7.  **Theme1.epic1.story7** (4pts)
8.  **Theme1.epic1.story8** (4pts)
9.  **Theme1.epic1.story9** (4pts)
10. **Theme1.epic1.story10** (4pts)
11. **Theme1.epic1.story11** (4pts)
12. **Theme1.epic1.story12** (4pts)
13. **Theme1.epic1.story13**  (2pts)

14. **Theme2.epic1.story1**  (2pts)
16. **Theme2.epic1.story2**  (2pts)
17. **Theme2.epic1.story3**  (4pts)
18. **Theme2.epic1.story4**  (2pts)


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
