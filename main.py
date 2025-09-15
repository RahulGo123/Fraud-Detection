from frauddetection.components.data_ingestion import DataIngestion
from frauddetection.exception.exception import FraudDetectionException
from frauddetection.logging.logger import logging
from frauddetection.entity.config_entity import DataIngestionConfig
from frauddetection.entity.config_entity import TrainingPipelineConfig


import sys

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiate the Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(data_ingestion_artifact)

    except Exception as e:
        raise FraudDetectionException(e, sys)