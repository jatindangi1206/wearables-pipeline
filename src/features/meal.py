import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .base import BaseFeatureExtractor
from .utils import standardize_timestamp_col

class MealFeaturesExtractor(BaseFeatureExtractor):
    """
    Extracts features from meal data, such as timing and regularity.
    """
    def extract_features(self) -> Dict[str, Any]:

        meal_data = self.data.get('meal', [])

        if len(meal_data) < 2:
            return {}

        df = pd.DataFrame([d.model_dump() for d in meal_data])
        df = standardize_timestamp_col(df)

        if 'timestamp' not in df.columns:
            return {}

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        if len(df) < 2:
            return {}
        df = df.sort_values('timestamp')

        features = {}

        inter_meal_intervals = df['timestamp'].diff().dt.total_seconds().dropna()
        if not inter_meal_intervals.empty:
            features['avg_inter_meal_interval_hours'] = inter_meal_intervals.mean() / 3600
            features['longest_fasting_window_hours'] = inter_meal_intervals.max() / 3600

        meal_times_seconds = df['timestamp'].dt.hour * 3600 + df['timestamp'].dt.minute * 60 + df['timestamp'].dt.second
        if len(meal_times_seconds) > 1:
            features['meal_time_variance_seconds'] = meal_times_seconds.var()

        dense_periods_count = 0
        if len(df) >= 3:
            for i in range(len(df) - 2):
                if (df['timestamp'].iloc[i+2] - df['timestamp'].iloc[i]) < pd.Timedelta(hours=6):
                    dense_periods_count += 1

        features['num_dense_eating_periods'] = dense_periods_count

        return {k: v for k, v in features.items() if pd.notna(v)}
