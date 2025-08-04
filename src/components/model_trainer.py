import os
import sys
import joblib
import numpy as np
from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from src.logger import logging
from src.exception import CustomException


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()

    def initiate_model_training(self, X_train, X_test, y_train, y_test):
        try:
            logging.info("Starting model training")

            model = LogisticRegression()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)

            logging.info(f"Model Accuracy: {acc}")
            logging.info(
                "Classification Report:\n" + classification_report(y_test, y_pred)
            )

            # Save model
            joblib.dump(model, self.config.trained_model_file_path)
            logging.info("Model saved successfully")

            return acc  # Return accuracy for logging or dashboard

        except Exception as e:
            raise CustomException(e, sys)
