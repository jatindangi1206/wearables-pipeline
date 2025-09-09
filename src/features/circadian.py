import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .base import BaseFeatureExtractor
from .utils import standardize_timestamp_col

class CircadianFeaturesExtractor(BaseFeatureExtractor):
    """
    Extracts circadian and time-of-day features from physiological data.
    """
    def extract_features(self) -> Dict[str, Any]:

        physio_keys = ['blood_pressure', 'heart_rate', 'sleep', 'spo2', 'steps', 'temperature']
        physio_data_dicts = []
        for key in physio_keys:
            for model_instance in self.data.get(key, []):
                physio_data_dicts.append(model_instance.model_dump())

        if not physio_data_dicts:
            return {}

        df = pd.DataFrame(physio_data_dicts)
        df = standardize_timestamp_col(df)

        if 'timestamp' not in df.columns:
            return {}
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        if df.empty:
            return {}
        df = df.set_index('timestamp')

        numeric_df = df.select_dtypes(include=np.number)
        if numeric_df.empty:
            return {}

        features = {}

        # 1. Average metrics by hour
        hourly_avg = numeric_df.resample('h').mean()
        features['hourly_avg'] = {
            k.isoformat(): v for k, v in hourly_avg.to_dict(orient='index').items()
        }

        # 2. Average metrics by time segments
        morning_avg = numeric_df.between_time('06:00', '12:00').mean().to_dict()
        afternoon_avg = numeric_df.between_time('12:00', '18:00').mean().to_dict()
        evening_avg = numeric_df.between_time('18:00', '23:59').mean().to_dict()
        night_avg = numeric_df.between_time('00:00', '05:59').mean().to_dict()
        features['time_segment_avg'] = {
            'morning': {k: v for k, v in morning_avg.items() if pd.notna(v)},
            'afternoon': {k: v for k, v in afternoon_avg.items() if pd.notna(v)},
            'evening': {k: v for k, v in evening_avg.items() if pd.notna(v)},
            'night': {k: v for k, v in night_avg.items() if pd.notna(v)},
        }

        # 3. Weekday vs Weekend comparison
        numeric_df_copy = numeric_df.copy()
        numeric_df_copy['weekday'] = numeric_df_copy.index.weekday
        weekday_df = numeric_df_copy[numeric_df_copy['weekday'] < 5]
        weekend_df = numeric_df_copy[numeric_df_copy['weekday'] >= 5]

        weekday_avg = weekday_df.drop(columns=['weekday']).mean().to_dict()
        weekend_avg = weekend_df.drop(columns=['weekday']).mean().to_dict()

        features['weekday_vs_weekend'] = {
            'weekday_avg': {k: v for k, v in weekday_avg.items() if pd.notna(v)},
            'weekend_avg': {k: v for k, v in weekend_avg.items() if pd.notna(v)},
        }

        return features
