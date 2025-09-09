import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .base import BaseFeatureExtractor
from .utils import standardize_timestamp_col

# Import antropy, but handle ImportError if not installed
try:
    import antropy as ant
except ImportError:
    ant = None

class ComplexityFeaturesExtractor(BaseFeatureExtractor):
    """
    Extracts complexity and nonlinear features from time-series data.
    """
    def extract_features(self) -> Dict[str, Any]:
        if ant is None:
            # antropy is not installed, so we can't extract these features.
            return {"error": "antropy library not installed. Please install it to use complexity features."}

        features = {}

        # --- Process Heart Rate Data ---
        hr_data = self.data.get('heart_rate', [])
        if hr_data:
            df_hr = pd.DataFrame([d.model_dump() for d in hr_data])
            df_hr = standardize_timestamp_col(df_hr)
            if 'timestamp' in df_hr.columns:
                df_hr['timestamp'] = pd.to_datetime(df_hr['timestamp'], errors='coerce')
                df_hr = df_hr.dropna(subset=['timestamp']).set_index('timestamp').sort_index()

                series = df_hr['heart_rate'].dropna()
                if not series.empty and pd.api.types.is_numeric_dtype(series) and len(series) >= 10:
                    col_features = {}
                    try:
                        col_features['approximate_entropy'] = ant.app_entropy(series)
                    except Exception:
                        col_features['approximate_entropy'] = None
                    try:
                        col_features['sample_entropy'] = ant.sample_entropy(series)
                    except Exception:
                        col_features['sample_entropy'] = None
                    features['heart_rate'] = {k: v for k, v in col_features.items() if pd.notna(v)}

        # --- Process SpO2 Data ---
        spo2_data = self.data.get('spo2', [])
        if spo2_data:
            df_spo2 = pd.DataFrame([d.model_dump() for d in spo2_data])
            df_spo2 = standardize_timestamp_col(df_spo2)
            if 'timestamp' in df_spo2.columns:
                df_spo2['timestamp'] = pd.to_datetime(df_spo2['timestamp'], errors='coerce')
                df_spo2 = df_spo2.dropna(subset=['timestamp']).set_index('timestamp').sort_index()

                series = df_spo2['spo2_value'].dropna()
                if not series.empty and pd.api.types.is_numeric_dtype(series) and len(series) >= 10:
                    col_features = {}
                    try:
                        col_features['approximate_entropy'] = ant.app_entropy(series)
                    except Exception:
                        col_features['approximate_entropy'] = None
                    try:
                        col_features['sample_entropy'] = ant.sample_entropy(series)
                    except Exception:
                        col_features['sample_entropy'] = None
                    features['spo2_value'] = {k: v for k, v in col_features.items() if pd.notna(v)}

        return features
