import yaml
from typing import List, Dict
from .models import data_models
from .processors.csv_processor import CsvProcessor
from .processors.json_processor import JsonProcessor
from .processors.specialized import HeartRateProcessor
from .utils.timestamp import convert_timestamp_cols

def get_processor(source_type: str, file_path: str, model, schema_mapping: dict):
    if source_type == 'csv':
        return CsvProcessor(file_path, model, schema_mapping)
    elif source_type == 'json':
        return JsonProcessor(file_path, model, schema_mapping)
    elif source_type == 'heart_rate':
        return HeartRateProcessor(file_path, model, schema_mapping)
    else:
        raise ValueError(f"Unknown source type: {source_type}")

def ingest_data(config_path: str) -> Dict[str, List]:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    all_data = {}
    for source_name, source_config in config['data_sources'].items():
        model = getattr(data_models, source_config['model'])
        processor = get_processor(
            source_config['type'],
            source_config['file_path'],
            model,
            source_config['schema_mapping']
        )
        processed_data = processor.process()
        # Convert Unix timestamps to human-readable date/time
        processed_data = convert_timestamp_cols(processed_data)
        all_data[source_name] = processed_data
    
    return all_data