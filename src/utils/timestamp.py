import pandas as pd
from datetime import datetime

def convert_timestamp_cols(data):
    """
    Converts Unix timestamp columns to human-readable date/time in DataFrames or lists of dicts.
    """
    if isinstance(data, pd.DataFrame):
        for col in data.columns:
            if 'time' in col.lower() or 'date' in col.lower():
                if pd.api.types.is_numeric_dtype(data[col]):
                    data[col] = pd.to_datetime(data[col], unit='s')
        return data
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        for row in data:
            for key, value in row.items():
                if ('time' in key.lower() or 'date' in key.lower()) and isinstance(value, (int, float)):
                    # Convert Unix timestamp to ISO 8601 string
                    try:
                        row[key] = datetime.utcfromtimestamp(value).isoformat()
                    except Exception:
                        pass
        return data
    else:
        return data