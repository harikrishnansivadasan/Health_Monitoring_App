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

    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Reading training and test data")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Drop unwanted columns if any
            cols_to_drop = ["Age"] if "Age" in train_df.columns else []
            train_df = train_df.drop(columns=cols_to_drop, errors="ignore")
            test_df = test_df.drop(columns=cols_to_drop, errors="ignore")

            # Separate features and target
            target_column = "Condition_Worsening"
            X_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]

            X_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            # Preprocessing
            preprocessor = self.get_preprocessor()
            X_train_scaled = preprocessor.fit_transform(X_train)
            X_test_scaled = preprocessor.transform(X_test)

            joblib.dump(preprocessor, self.config.preprocessor_obj_file_path)
            logging.info("Data transformation completed")

            return (
                X_train_scaled,
                X_test_scaled,
                y_train.to_numpy(),
                y_test.to_numpy(),
            )

        except Exception as e:
            raise CustomException(e, sys)
