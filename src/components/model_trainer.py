import os
import sys
import joblib
import numpy as np
from dataclasses import dataclass
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from src.logger import logging
from src.exception import CustomException


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "dbscan_model.pkl")


class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()

    def initiate_model_training(self, X, eps=0.5, min_samples=5):
        try:
            logging.info("Starting DbScan model training")

            model = DBSCAN(eps=eps, min_samples=min_samples)
            cluster_labels = model.fit_predict(X)

            # silhouette score eval
            labels_for_score = cluster_labels[cluster_labels != -1]
            X_for_score = X[cluster_labels != -1]

            if len(set(labels_for_score)) > 1:
                sil_score = silhouette_score(X_for_score, labels_for_score)
                logging.info(f"Silhouette score (excluding noise): {sil_score}")
            else:
                sil_score = -1
                logging.warning("Silhouette score not defined for less than 2 clusters")

            # Save model
            joblib.dump(model, self.config.trained_model_file_path)
            logging.info("DBScan Model saved successfully")

            return sil_score, cluster_labels  # Return silh scoere
        except Exception as e:
            raise CustomException(e, sys)
