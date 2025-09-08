from abc import ABC, abstractmethod
from typing import List, Type
from pydantic import BaseModel

class BaseProcessor(ABC):
    def __init__(self, file_path: str, model: Type[BaseModel], schema_mapping: dict):
        self.file_path = file_path
        self.model = model
        self.schema_mapping = schema_mapping

    @abstractmethod
    def process(self) -> List[BaseModel]:
        raise NotImplementedError

    def _rename_columns(self, df):
        return df.rename(columns=self.schema_mapping)

    def _validate_data(self, df):
        records = df.to_dict(orient='records')
        return [self.model(**record) for record in records]