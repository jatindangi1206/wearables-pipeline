import pandas as pd
from typing import List
from .base import BaseProcessor
from ..utils.timestamp import convert_timestamp_cols

class JsonProcessor(BaseProcessor):
    def process(self) -> List:
        df = pd.read_json(self.file_path)
        df = self._rename_columns(df)
        df = convert_timestamp_cols(df)
        
        # Ensure only columns from the schema mapping are present
        mapped_cols = [col for col in self.schema_mapping.values() if col in df.columns]
        df = df[mapped_cols]
        
        return self._validate_data(df)