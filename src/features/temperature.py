import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .base import BaseFeatureExtractor
from .utils import standardize_timestamp_col

class TemperatureFeaturesExtractor(BaseFeatureExtractor):
    """
    Extracts features from temperature data, including its relationship with other physiological signals.
    """
    def extract_features(self) -> Dict[str, Any]:

        temp_data = self.data.get('temperature', [])
        hr_data = self.data.get('heart_rate', [])
        spo2_data = self.data.get('spo2', [])

        if not temp_data:
            return {}

        df_temp = pd.DataFrame([d.model_dump() for d in temp_data])
        df_temp = standardize_timestamp_col(df_temp)

        if 'timestamp' not in df_temp.columns:
            return {}
        df_temp['timestamp'] = pd.to_datetime(df_temp['timestamp'], errors='coerce')
        df_temp = df_temp.dropna(subset=['timestamp']).set_index('timestamp').sort_index()

        features = {}

        temp_series = df_temp['temperature'].dropna()
        if not temp_series.empty:
            features['daily_temperature_amplitude'] = temp_series.resample('D').apply(lambda x: x.max() - x.min() if len(x) > 0 else 0).mean()
            baseline_temp = 37.0
            features['avg_deviation_from_baseline'] = (temp_series - baseline_temp).abs().mean()

        resample_freq = '15min'
        temp_series_resampled = temp_series.resample(resample_freq).mean()

        if hr_data:
            df_hr = pd.DataFrame([d.model_dump() for d in hr_data])
            df_hr = standardize_timestamp_col(df_hr)
            if 'timestamp' in df_hr.columns:
                df_hr['timestamp'] = pd.to_datetime(df_hr['timestamp'], errors='coerce')
                df_hr = df_hr.dropna(subset=['timestamp']).set_index('timestamp').sort_index()
                hr_series = df_hr['heart_rate'].dropna()
                if not hr_series.empty and not temp_series_resampled.empty:
                    hr_resampled = hr_series.resample(resample_freq).mean()
                    aligned_df = pd.concat([temp_series_resampled, hr_resampled], axis=1, keys=['temp', 'hr']).dropna()
                    if len(aligned_df) > 1:
                        features['cross_corr_temp_hr'] = aligned_df['temp'].corr(aligned_df['hr'])

        if spo2_data:
            df_spo2 = pd.DataFrame([d.model_dump() for d in spo2_data])
            df_spo2 = standardize_timestamp_col(df_spo2)
            if 'timestamp' in df_spo2.columns:
                df_spo2['timestamp'] = pd.to_datetime(df_spo2['timestamp'], errors='coerce')
                df_spo2 = df_spo2.dropna(subset=['timestamp']).set_index('timestamp').sort_index()
                spo2_series = df_spo2['spo2_value'].dropna()
                if not spo2_series.empty and not temp_series_resampled.empty:
                    spo2_resampled = spo2_series.resample(resample_freq).mean()
                    aligned_df = pd.concat([temp_series_resampled, spo2_resampled], axis=1, keys=['temp', 'spo2']).dropna()
                    if len(aligned_df) > 1:
                        features['cross_corr_temp_spo2'] = aligned_df['temp'].corr(aligned_df['spo2'])

        return {k: v for k, v in features.items() if pd.notna(v)}
