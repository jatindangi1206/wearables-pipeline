import pandas as pd
from typing import List
from .base import BaseProcessor
from ..utils.timestamp import convert_timestamp_cols

class CsvProcessor(BaseProcessor):
    def process(self) -> List:
        df = pd.read_csv(self.file_path)
        df = self._rename_columns(df)
        df = convert_timestamp_cols(df)
        
        # Calculate FVC for lung function data
        if 'fev1' in df.columns and 'fev1_fvc' in df.columns:
            # Ensure fev1_fvc is not zero to avoid division by zero
            df['fvc'] = df.apply(lambda row: row['fev1'] / row['fev1_fvc'] if row['fev1_fvc'] != 0 else 0, axis=1)

        # Fill NaN values with empty strings for object columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna('')

        # Ensure only columns from the schema mapping (and calculated columns) are present
        model_fields = list(self.model.model_fields.keys())
        present_cols = [col for col in df.columns if col in model_fields]
        df = df[present_cols]
        
        return self._validate_data(df)