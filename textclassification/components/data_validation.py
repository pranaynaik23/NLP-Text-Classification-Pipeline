import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.feature_extraction.text import CountVectorizer
import yaml
import shutil
from textclassification.logger import logging
from textclassification.exception import CustomException
from textclassification.entity.config_entity import DataValidationConfig
from textclassification.entity.artifact_entity import DataIngestionArtifacts ,DataValidationArtifacts

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifacts):
        try:
            
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try: 
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys) from e

    def get_expected_columns(self, file_path):
        """
        Get the expected number of columns from the ingested data file.
        """
        try:
            data = DataValidation.read_data(file_path)
            return data.shape[1]
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def get_expected_features(self, file_path):
        """
        Get the expected number of columns from the ingested data file.
        """
        try:
            data = DataValidation.read_data(file_path)
            features = list(data.columns)
            return features
        except Exception as e:
            raise CustomException(e, sys) from e

    def validate_number_of_columns(self, file_path, expected_columns):
        """
        Validates if the number of columns in the given file matches the expected number of columns.
        """
        try:
            data = DataValidation.read_data(file_path)
            if data.shape[1] != expected_columns:
                return False
            return True
        except Exception as e:
            raise CustomException(e, sys) from e

    def detect_data_drift(self, base_file_path, current_file_path, feature_column, threshold=0.05):
        """
        Detects data drift in the feature column between the base file and the current file.
        """
        try:
            # Load data
            base_data = DataValidation.read_data(base_file_path)
            current_data = DataValidation.read_data(current_file_path)

            # Vectorize text data
            vectorizer = CountVectorizer()
            base_vectorized = vectorizer.fit_transform(base_data[feature_column])
            current_vectorized = vectorizer.transform(current_data[feature_column])

            # Calculate frequency distributions
            base_freq = np.mean(base_vectorized.toarray(), axis=0)
            current_freq = np.mean(current_vectorized.toarray(), axis=0)

            # Create contingency table
            contingency_table = np.array([base_freq, current_freq])
            _, p_value, _, _ = chi2_contingency(contingency_table)

            # Check if p-value is less than the threshold
            data_drift_detected = p_value < threshold

            # Save the report
            report = {
                'p_value': p_value,
                'data_drift_detected': data_drift_detected
            }

            os.makedirs(os.path.dirname(self.data_validation_config.drift_report_file_path), exist_ok=True)
            with open(self.data_validation_config.drift_report_file_path, 'w') as file:
                yaml.dump(report, file)

            return data_drift_detected
        except Exception as e:
            raise CustomException(e, sys) from e
    
    

    def initiate_data_validation(self) -> DataValidationArtifacts:
        logging.info("Entered the initiate_data_validation method of Data Validation class")
        os.makedirs(self.data_validation_config.DATA_VALIDATION_ARTIFACTS_DIR, exist_ok=True)
        os.makedirs(self.data_validation_config.VALID_DATA_DIR,exist_ok=True)
        os.makedirs(self.data_validation_config.INVALID_DATA_DIR,exist_ok=True)
        try:
            
            logging.info("Checking base file path for imbalanced data comparison")
            if not os.path.isfile(self.data_validation_config.VALID_IMBALANCED_DATA_FILE_PATH):
                base_file_path_imbalanced = self.data_ingestion_artifact.imbalance_data_file_path
                shutil.copy(self.data_ingestion_artifact.imbalance_data_file_path,self.data_validation_config.VALID_IMBALANCED_DATA_FILE_PATH)
            else:
                base_file_path_imbalanced = self.data_validation_config.VALID_IMBALANCED_DATA_FILE_PATH
            logging.info(f"base_file_path={base_file_path_imbalanced}")

            logging.info("Checking base file path for raw data comparison")
            if not os.path.isfile(self.data_validation_config.VALID_RAW_DATA_FILE_PATH):
                base_file_path_raw = self.data_ingestion_artifact.raw_data_file_path
                shutil.copy(self.data_ingestion_artifact.raw_data_file_path,self.data_validation_config.VALID_RAW_DATA_FILE_PATH)
            else:
                base_file_path_raw = self.data_validation_config.VALID_RAW_DATA_FILE_PATH
            logging.info(f"base_file_path={base_file_path_raw}")
            
            logging.info("Getting number of columns from basefile")
            len_columns_imbalanced = self.get_expected_columns(file_path=base_file_path_imbalanced)
            len_columns_raw = self.get_expected_columns(file_path=base_file_path_raw)
            logging.info("No. of columns extracted")

            logging.info("Getting features from basefile")
            features_imbalanced = self.get_expected_features(file_path=base_file_path_imbalanced)
            features_raw = self.get_expected_features(file_path=base_file_path_raw)
            logging.info("Features extracted")

            logging.info("Validating No. of Columns ")
            validation_columns_imbalanced = self.validate_number_of_columns(file_path=self.data_ingestion_artifact.imbalance_data_file_path,expected_columns=len_columns_imbalanced)
            validation_columns_raw = self.validate_number_of_columns(file_path=self.data_ingestion_artifact.imbalance_data_file_path,expected_columns=len_columns_imbalanced)
            logging.info("Validated No. of Columns ")

            logging.info("Validating Data Drfit")
            data_drift_imbalanced = self.detect_data_drift(base_file_path=base_file_path_imbalanced,current_file_path=self.data_ingestion_artifact.imbalance_data_file_path,feature_column="tweet")
            data_drift_raw = self.detect_data_drift(base_file_path=base_file_path_raw,current_file_path=self.data_ingestion_artifact.raw_data_file_path,feature_column="tweet")
            logging.info("Validated Data Drfit")

            if validation_columns_imbalanced & data_drift_imbalanced:
                logging.info("Current Imbalanced data is valid and can be used for further transformations")
                shutil.copy(self.data_ingestion_artifact.imbalance_data_file_path,self.data_validation_config.VALID_IMBALANCED_DATA_FILE_PATH)
            else:
                logging.info("Current Imbalanced data is not valid and cannot be used for further transformations")
                shutil.copy(self.data_ingestion_artifact.imbalance_data_file_path,self.data_validation_config.INVALID_IMBALANCED_DATA_FILE_PATH)

            if validation_columns_raw & data_drift_raw:
                logging.info("Current Raw data is valid and can be used for further transformations")
                shutil.copy(self.data_ingestion_artifact.raw_data_file_path,self.data_validation_config.VALID_RAW_DATA_FILE_PATH)
            
            else:
                logging.info("Current Raw data is not valid and cannot be used for further transformations")
                shutil.copy(self.data_ingestion_artifact.raw_data_file_path,self.data_validation_config.INVALID_RAW_DATA_FILE_PATH)




            data_validation_artifacts = DataValidationArtifacts(
            validation_status = (validation_columns_imbalanced & data_drift_imbalanced) & (validation_columns_raw & data_drift_raw),
            valid_imbalance_data_file_path = self.data_validation_config.VALID_IMBALANCED_DATA_FILE_PATH,
            valid_raw_data_file_path = self.data_validation_config.VALID_RAW_DATA_FILE_PATH,
            invalid_imbalance_data_file_path = self.data_validation_config.INVALID_IMBALANCED_DATA_FILE_PATH,
            invalid_raw_data_file_path =self.data_validation_config.INVALID_RAW_DATA_FILE_PATH,
            drift_report_file_path= self.data_validation_config.drift_report_file_path
            )

            logging.info("Exited the initiate_data_validation method of Data Validation class")

            logging.info(f"Data Validation artifact: {data_validation_artifacts}")

            return data_validation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
            