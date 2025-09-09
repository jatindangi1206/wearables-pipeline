import pandas as pd
from typing import List
from .base import BaseProcessor
from ..utils.timestamp import convert_timestamp_cols

class CsvProcessor(BaseProcessor):
    def process(self) -> List:
        df = pd.read_csv(self.file_path)
        df = self._rename_columns(df)
        df = convert_timestamp_cols(df)
        
        # Fill NaN values with empty strings for object columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna('')

        # Drop columns that are not in the schema mapping
        df = df[self.schema_mapping.values()]
        
        return self._validate_data(df)