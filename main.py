from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    ingestion = DataIngestion()
    train_path, test_path, raw_path = ingestion.initiate_data_ingestion()
    print(train_path, test_path, raw_path)

    transformation = DataTransformation()
    X_scaled = transformation.initiate_data_transformation(data_path=raw_path)

    trainer = ModelTrainer()
    sil_score, cluster_labels = trainer.initiate_model_training(
        X_scaled, eps=1.2, min_samples=11
    )

    print(f"Training complete. Silhouette Score: {sil_score}")
    print(f"Cluster labels assigned: {set(cluster_labels)}")
