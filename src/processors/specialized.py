import pandas as pd
import json
from typing import List
from .base import BaseProcessor
from ..utils.timestamp import convert_timestamp_cols

class HeartRateProcessor(BaseProcessor):
    def process(self) -> List:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        df = pd.json_normalize(data, record_path=['jsonData'])
        df = self._rename_columns(df)
        df = convert_timestamp_cols(df)
        
        # Drop columns that are not in the schema mapping
        df = df[self.schema_mapping.values()]
        
        return self._validate_data(df)