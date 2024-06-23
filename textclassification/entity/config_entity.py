from dataclasses import dataclass
from textclassification.constants import *
import os

class DataIngestionConfig:
    def __init__(self):
        self.BUCKET_NAME = BUCKET_NAME
        self.ZIP_FILE_NAME = ZIP_FILE_NAME
        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR,DATA_INGESTION_ARTIFACTS_DIR)
        self.DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,DATA_INGESTION_IMBALANCE_DATA_DIR)
        self.NEW_DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,DATA_INGESTION_RAW_DATA_DIR)
        self.ZIP_FILE_DIR = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,self.ZIP_FILE_NAME)

class DataValidationConfig:

    def __init__(self):
        self.DATA_VALIDATION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR, DATA_VALIDATION_ARTIFACTS_DIR)
        self.VALID_DATA_DIR: str = os.path.join(self.DATA_VALIDATION_ARTIFACTS_DIR, DATA_VALIDATION_VALID_DIR)
        self.INVALID_DATA_DIR: str = os.path.join(self.DATA_VALIDATION_ARTIFACTS_DIR, DATA_VALIDATION_INVALID_DIR)
        self.VALID_IMBALANCED_DATA_FILE_PATH: str = os.path.join(self.VALID_DATA_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR)
        self.VALID_RAW_DATA_FILE_PATH: str = os.path.join(self.VALID_DATA_DIR, DATA_INGESTION_RAW_DATA_DIR)
        self.INVALID_IMBALANCED_DATA_FILE_PATH: str = os.path.join(self.INVALID_DATA_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR)
        self.INVALID_RAW_DATA_FILE_PATH: str = os.path.join(self.INVALID_DATA_DIR, DATA_INGESTION_RAW_DATA_DIR)
        self.drift_report_file_path: str = os.path.join( self.DATA_VALIDATION_ARTIFACTS_DIR, DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)