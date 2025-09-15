import os
import sys
import numpy as np
import pandas as pd

PIPELINE_NAME: str = "FraudDetection"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "creditcard.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

##################### DATA INGESTION #########################

DATA_INGESTION_COLLECTION_NAME = "FraudData"
DATA_INGESTION_DATABASE_NAME = "RAHULAI"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2