import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import joblib


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.config = DataTransformationConfig()

    def get_preprocessor(self):
        # Standardize all features
        scaler = StandardScaler()
        return scaler

    def initiate_data_transformation(self, data_path):
        try:
            logging.info("Reading training and test data")
            df = pd.read_csv(data_path)

            # Drop unwanted columns if any
            cols_to_drop = ["Age"] if "Age" in df.columns else []
            df = df.drop(columns=cols_to_drop, errors="ignore")

            # features 
            features = df.copy()

            # Preprocessing
            preprocessor = self.get_preprocessor()
            features_scaled = preprocessor.fit_transform(features)

            joblib.dump(preprocessor, self.config.preprocessor_obj_file_path)
            logging.info("Data transformation completed")

            return (
                features_scaled
            )

        except Exception as e:
            raise CustomException(e, sys)
