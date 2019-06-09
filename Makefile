data/heart_features.csv: config/config.yml
	python src/generate_features.py
data/x_test.npy: config/config.yml
	python src/train_model.py
data/y_test.npy: config/config.yml
	python src/train_model.py
data/model.pkl: config/config.yml
	python src/train_model.py
data/confusion_matrix.png: config/config.yml
	python src/score_model.py
data/CV_scores.csv: config/config.yml
	python src/score_model.py
data/CV_mean.csv: config/config.yml
	python src/score_model.py
all: config/config.yml
	python src/generate_features.py; python src/train_model.py; python src/score_model.py; 