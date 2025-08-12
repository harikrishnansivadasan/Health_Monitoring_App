import pandas as pd
import numpy as np
import joblib
import os
import sys
from src.exception import CustomException
from src.logger import logging
from sklearn.neighbors import NearestNeighbors

CLUSTER_LABELS = {
    0: "Stable",
    -1: "Risk ",
    1: "Critical ",
}

patient_cluster_history = {}


class PredictionPipeline:
    def __init__(self):
        try:
            logging.info("Loading model and scaler from artifacts")
            self.model = joblib.load(os.path.join("artifacts", "dbscan_model.pkl"))
            self.scaler = joblib.load(os.path.join("artifacts", "preprocessor.pkl"))
            logging.info("Model and scaler loaded successfully")

            # Extract eps parameter from model (needed for prediction)
            self.eps = getattr(self.model, "eps", 0.5)
            # Extract core samples for prediction heuristic
            self.core_samples = self.model.components_  # core points in feature space

            # NearestNeighbors model on core samples for assignment
            self.nn = NearestNeighbors(radius=self.eps).fit(self.core_samples)

        except Exception as e:
            logging.error("Failed to load model or scaler")
            raise CustomException(e, sys)

    def _generate_alert(self, patient_id, current_cluster):
        """Generate early warning based on cluster transitions."""

        current_status = CLUSTER_LABELS.get(current_cluster, "Unknown")
        prev_cluster = patient_cluster_history.get(patient_id)

        patient_cluster_history[patient_id] = current_cluster  # Update history

        if prev_cluster is not None:
            if prev_cluster == 0 and current_cluster in [-1, 1]:
                return f" Early Warning: Moved from Stable to {current_status}"
            elif prev_cluster == -1 and current_cluster == 1:
                return f" Critical Alert: Worsened to Critical"

        return f"Status: {current_status}"

    def predict(self, input_df: pd.DataFrame, patient_id="ASG123"):
        try:
            logging.info(f"Received input for prediction: {input_df.shape}")

            # Input validation
            if input_df.isnull().any().any():
                raise ValueError("Input data contains missing values.")

            # Scale the input data
            logging.info("Scaling input data")
            scaled_data = self.scaler.transform(input_df)

            # Predict
            logging.info("Assigning cluster labels based on DBSCAN core samples")
            distances, indices = self.nn.radius_neighbors(
                scaled_data, return_distance=True
            )
            predicted_labels = []

            for dist, inds in zip(distances, indices):
                if len(inds) == 0:
                    # No core point within eps radius => noise
                    predicted_labels.append(-1)
                else:
                    # Assign cluster label of nearest core point
                    # The core_samples_ are ordered by model.labels_ of core points
                    core_point_idx = inds[np.argmin(dist)]
                    predicted_labels.append(
                        self.model.labels_[
                            self.model.core_sample_indices_[core_point_idx]
                        ]
                    )

            predicted_labels = np.array(predicted_labels)

            # Generate alerts for each sample
            alerts = [
                self._generate_alert(patient_id, cluster)
                for cluster in predicted_labels
            ]

            logging.info("Prediction and alert generation completed")
            return {"clusters": predicted_labels[0], "alerts": alerts[0]}

        except Exception as e:
            logging.error("Error occurred during prediction")
            raise CustomException(e, sys)
