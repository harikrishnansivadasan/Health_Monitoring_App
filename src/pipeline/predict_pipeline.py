import pandas as pd
import joblib
import os
import sys
from src.exception import CustomException
from src.logger import logging


class PredictionPipeline:
    def __init__(self):
        try:
            logging.info("Loading model and scaler from artifacts")
            self.model = joblib.load(os.path.join("artifacts", "model.pkl"))
            self.scaler = joblib.load(os.path.join("artifacts", "preprocessor.pkl"))
            logging.info("Model and scaler loaded successfully")
        except Exception as e:
            logging.error("Failed to load model or scaler")
            raise CustomException(e, sys)

    def predict(self, input_df: pd.DataFrame):
        try:
            logging.info(f"Received input for prediction: {input_df.shape}")

            # Input validation
            if input_df.isnull().any().any():
                raise ValueError("Input data contains missing values.")

            # Scale the input data
            logging.info("Scaling input data")
            scaled_data = self.scaler.transform(input_df)

            # Predict
            logging.info("Making predictions")
            predictions = self.model.predict(scaled_data)

            logging.info("Prediction completed")
            return predictions

        except Exception as e:
            logging.error("Error occurred during prediction")
            raise CustomException(e, sys)
