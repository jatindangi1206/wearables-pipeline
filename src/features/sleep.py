import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .base import BaseFeatureExtractor
from .utils import standardize_timestamp_col

class SleepFeaturesExtractor(BaseFeatureExtractor):
    """
    Extracts sleep-specific features, focusing on heart rate dynamics during sleep.
    """
    def extract_features(self) -> Dict[str, Any]:

        sleep_data = self.data.get('sleep', [])
        hr_data = self.data.get('heart_rate', [])

        if not sleep_data or not hr_data:
            return {}

        df_sleep = pd.DataFrame([d.model_dump() for d in sleep_data])
        df_hr = pd.DataFrame([d.model_dump() for d in hr_data])

        df_sleep = standardize_timestamp_col(df_sleep)
        if 'log_end_time' in df_sleep.columns:
            df_sleep = df_sleep.rename(columns={'log_end_time': 'timestamp_end'})

        df_hr = standardize_timestamp_col(df_hr)

        if 'timestamp' not in df_sleep.columns or 'timestamp_end' not in df_sleep.columns or 'timestamp' not in df_hr.columns:
            return {}

        df_sleep['timestamp'] = pd.to_datetime(df_sleep['timestamp'], errors='coerce')
        df_sleep['timestamp_end'] = pd.to_datetime(df_sleep['timestamp_end'], errors='coerce')
        df_hr['timestamp'] = pd.to_datetime(df_hr['timestamp'], errors='coerce')

        df_sleep = df_sleep.dropna(subset=['timestamp', 'timestamp_end']).set_index('timestamp').sort_index()
        df_hr = df_hr.dropna(subset=['timestamp']).set_index('timestamp').sort_index()

        if df_sleep.empty or df_hr.empty:
            return {}

        features = {}

        for i, session in df_sleep.iterrows():
            session_start = i
            session_end = session['timestamp_end']

            hr_in_sleep = df_hr['heart_rate'][session_start:session_end]

            if len(hr_in_sleep) < 2:
                continue

            session_features = {}

            lowest_hr_time = hr_in_sleep.idxmin()
            time_to_lowest_hr = (lowest_hr_time - session_start).total_seconds()
            session_features['time_to_lowest_hr_seconds'] = time_to_lowest_hr

            hr_first_30min = hr_in_sleep[session_start : session_start + pd.Timedelta(minutes=30)]
            if len(hr_first_30min) > 1:
                x = (hr_first_30min.index - session_start).total_seconds().values
                y = hr_first_30min.values
                try:
                    slope, _ = np.polyfit(x, y, 1)
                    session_features['hr_onset_slope'] = slope
                except Exception:
                    session_features['hr_onset_slope'] = None

            hr_last_30min = hr_in_sleep[session_end - pd.Timedelta(minutes=30) : session_end]
            if len(hr_last_30min) > 1:
                x = (hr_last_30min.index - (session_end - pd.Timedelta(minutes=30))).total_seconds().values
                y = hr_last_30min.values
                try:
                    slope, _ = np.polyfit(x, y, 1)
                    session_features['hr_wake_slope'] = slope
                except Exception:
                    session_features['hr_wake_slope'] = None

            features[str(session_start)] = {k: v for k, v in session_features.items() if pd.notna(v)}

        return {'sleep_hr_dynamics': features}
