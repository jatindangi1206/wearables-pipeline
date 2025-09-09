import pandas as pd
from typing import List
from .base import BaseProcessor
from ..utils.timestamp import convert_timestamp_cols

class JsonProcessor(BaseProcessor):
    def process(self) -> List:
        df = pd.read_json(self.file_path)
        df = self._rename_columns(df)
        df = convert_timestamp_cols(df)
        
        # Drop columns that are not in the schema mapping
        df = df[self.schema_mapping.values()]
        
        return self._validate_data(df)