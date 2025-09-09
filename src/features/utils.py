import pandas as pd

def standardize_timestamp_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames known timestamp columns to a standard 'timestamp' name.
    """
    rename_map = {
        'created_time': 'timestamp',
        'log_date_time': 'timestamp',
        'time': 'timestamp'
    }
    # Find which timestamp column exists and rename it
    for old_name, new_name in rename_map.items():
        if old_name in df.columns:
            df = df.rename(columns={old_name: new_name})
            break
    return df
