from abc import ABC, abstractmethod
from typing import List, Type
from pydantic import BaseModel, ValidationError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        validated_records = []
        for record in df.to_dict(orient='records'):
            try:
                validated_records.append(self.model(**record))
            except ValidationError as e:
                logger.warning(f"Validation error for record in {self.file_path}: {record}\n{e}")
        return validated_records