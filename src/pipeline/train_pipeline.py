from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging
from src.exception import CustomException
import sys

if __name__ == "__main__":
    try:
        logging.info("start ingestion")
        ingestion = DataIngestion()

        train_path, test_path, raw_path = ingestion.initiate_data_ingestion()
        print(train_path, test_path, raw_path)
        logging.info(
            f"Data ingestion complete: train_path={train_path}, test_path={test_path}, raw_path={raw_path}"
        )

        logging.info("Starting data transformation")
        transformation = DataTransformation()
        X_scaled = transformation.initiate_data_transformation(data_path=raw_path)

        logging.info("Starting model training")
        trainer = ModelTrainer()
        sil_score, cluster_labels = trainer.initiate_model_training(
            X_scaled, eps=0.6, min_samples=4
        )
        logging.info(f"Model training complete. Silhouette Score: {sil_score}")
        logging.info(f"Cluster labels assigned: {set(cluster_labels)}")

        print(f"Training complete. Silhouette Score: {sil_score}")
        print(f"Cluster labels assigned: {set(cluster_labels)}")

    except Exception as e:
        logging.error("Error occurred during training pipeline execution")
        raise CustomException(e, sys)
