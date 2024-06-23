from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
     imbalance_data_file_path: str
     raw_data_file_path: str

@dataclass
class DataValidationArtifacts:
    validation_status: bool
    valid_imbalance_data_file_path: str
    valid_raw_data_file_path: str
    invalid_imbalance_data_file_path: str
    invalid_raw_data_file_path: str
    drift_report_file_path: str

