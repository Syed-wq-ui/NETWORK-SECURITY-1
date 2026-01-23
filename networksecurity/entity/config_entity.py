from datetime import datetime
import os
from networksecurity.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp: str = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Base directory for data ingestion
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, 
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # Path to the feature store (raw data)
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, 
            training_pipeline.DATA_INGESTION_FEATURE_FILE_NAME
        )

        # Path to the training file
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            training_pipeline.DATA_INGESTION_INGESTED_DIR, 
            training_pipeline.DATA_INGESTION_TRAIN_DIR, 
            training_pipeline.DATA_INGESTION_TRAIN_FILE_NAME
        )

        # Path to the testing file
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, 
            training_pipeline.DATA_INGESTION_INGESTED_DIR, 
            training_pipeline.DATA_INGESTION_TEST_DIR, 
            training_pipeline.DATA_INGESTION_TEST_FILE_NAME
        )

        # Other metadata
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME