import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .base import BaseFeatureExtractor
from .utils import standardize_timestamp_col

class ActivityFeaturesExtractor(BaseFeatureExtractor):
    """
    Extracts features from activity and step data.
    """
    def extract_features(self) -> Dict[str, Any]:

        steps_data = self.data.get('steps', [])

        if not steps_data:
            return {}

        df = pd.DataFrame([d.model_dump() for d in steps_data])
        df = standardize_timestamp_col(df)

        if 'log_end_time' in df.columns:
            df = df.rename(columns={'log_end_time': 'timestamp_end'})

        required_cols = ['timestamp', 'steps', 'distance', 'timestamp_end']
        if not all(col in df.columns for col in required_cols):
            return {}

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['timestamp_end'] = pd.to_datetime(df['timestamp_end'], errors='coerce')
        df = df.dropna(subset=required_cols)
        if df.empty:
            return {}
        df = df.set_index('timestamp').sort_index()

        features = {}

        df['duration_seconds'] = (df['timestamp_end'] - df.index).dt.total_seconds()
        df_valid_duration = df[df['duration_seconds'] > 0].copy()
        if not df_valid_duration.empty:
            df_valid_duration['cadence'] = df_valid_duration['steps'] / (df_valid_duration['duration_seconds'] / 60)
            features['average_cadence'] = df_valid_duration['cadence'].mean()
            features['average_pace_mps'] = (df_valid_duration['distance'] / df_valid_duration['duration_seconds']).mean()

        step_threshold = 100
        df['is_burst'] = df['steps'] > step_threshold

        bursts = df[df['is_burst']]
        features['num_activity_bursts'] = len(bursts)
        if not bursts.empty:
            features['avg_burst_duration_seconds'] = bursts['duration_seconds'].mean()

        rest_periods = df[~df['is_burst']]
        features['num_rest_periods'] = len(rest_periods)

        return {k: v for k, v in features.items() if pd.notna(v)}
