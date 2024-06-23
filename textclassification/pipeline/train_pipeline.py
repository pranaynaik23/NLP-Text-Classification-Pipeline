import sys
from textclassification.logger import logging
from textclassification.exception import CustomException
from textclassification.components.data_ingestion import DataIngestion
from textclassification.components.data_validation import DataValidation

from textclassification.entity.config_entity import DataIngestionConfig,DataValidationConfig

from textclassification.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()


    

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from GCLoud Storage bucket")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)

            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train and valid from GCLoud Storage")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
    
    def start_data_validation(self, data_ingestion_artifacts = DataIngestionArtifacts) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_valiation method of TrainPipeline class")
        try:
            data_validation = DataValidation(
                data_validation_config= self.data_validation_config,
                data_ingestion_artifact=data_ingestion_artifacts
            )

            data_validation_artifacts = data_validation.initiate_data_validation()
            
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
    
    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts = data_ingestion_artifacts)
            
            logging.info("Exited the run_pipeline method of TrainPipeline class") 

        except Exception as e:
            raise CustomException(e, sys) from e
