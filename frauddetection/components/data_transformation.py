from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np
import os
import sys

from frauddetection.constant.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)
from frauddetection.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from frauddetection.entity.config_entity import DataTransformationConfig
from frauddetection.exception.exception import FraudDetectionException
from frauddetection.logging.logger import logging
from frauddetection.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        
        except Exception as e:
            raise FraudDetectionException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise FraudDetectionException(e, sys)
        
    def get_data_transformer_object(cls) ->Pipeline:
        logging.info("Entered get_data_transformer_object method of transformation class")
        
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise FraudDetectionException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered data Transformation")
        try:
            # 1. Read train and test CSVs
            train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            # 2. Separate input and target
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            # 3. Apply SMOTE only on training data
            smote = SMOTE(random_state=42)
            X_train_res, y_train_res = smote.fit_resample(input_feature_train_df, target_feature_train_df)

            # 4. Impute missing values using KNNImputer
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(X_train_res)

            transformed_input_train_feature = preprocessor_object.transform(X_train_res)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            # 5. Combine back input and target into arrays
            train_arr = np.c_[transformed_input_train_feature, np.array(y_train_res)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # 6. Save processed arrays and object
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            save_object("final_model/preprocessor.pkl", preprocessor_object)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact

        except Exception as e:
            raise FraudDetectionException(e, sys)

        