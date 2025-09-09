import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .base import BaseFeatureExtractor
from .utils import standardize_timestamp_col

class VariabilityFeaturesExtractor(BaseFeatureExtractor):
    """
    Extracts intra-day variability and dynamic features from time-series data.
    """
    def extract_features(self) -> Dict[str, Any]:

        hr_data = self.data.get('heart_rate', [])
        steps_data = self.data.get('steps', [])

        all_data_dicts = [d.model_dump() for d in hr_data] + [d.model_dump() for d in steps_data]

        if not all_data_dicts:
            return {}

        df = pd.DataFrame(all_data_dicts)
        df = standardize_timestamp_col(df)

        if 'timestamp' not in df.columns:
            return {}
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        if df.empty:
            return {}
        df = df.set_index('timestamp').sort_index()

        features = {}

        process_cols = ['heart_rate', 'steps']

        for col in process_cols:
            if col in df.columns:
                series = df[col].dropna()
                if series.empty or not pd.api.types.is_numeric_dtype(series):
                    continue

                col_features = {}

                rolling_window = series.rolling('15min')
                col_features['rolling_variance'] = rolling_window.var().mean()
                col_features['rolling_range'] = (rolling_window.max() - rolling_window.min()).mean()
                col_features['rolling_mad'] = rolling_window.apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True).mean()

                col_features['absolute_energy'] = np.sum(np.square(series))

                mean = series.mean()
                zero_crossings = np.sum(np.diff(np.sign(series - mean)) != 0)
                col_features['zero_crossing_rate'] = zero_crossings / len(series) if len(series) > 0 else 0

                features[col] = {k: v for k, v in col_features.items() if pd.notna(v)}

        return features
