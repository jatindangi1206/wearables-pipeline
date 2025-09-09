from typing import Dict, Any
from .base import BaseAnalyzer
from ..analysis_models.results import MealFeaturesAnalysisResult, PatternDetection

class MealFeaturesAnalyzer(BaseAnalyzer):
    """
    Analyzer for meal features.
    """
    def analyze(self) -> MealFeaturesAnalysisResult:
        features = self.data

        summary = self._summarize_meal_features(features)
        patterns = self._detect_patterns(features)

        return MealFeaturesAnalysisResult(
            summary=summary,
            patterns=PatternDetection(patterns=patterns, anomalies=[]),
            metadata=self.get_metadata()
        )

    def _summarize_meal_features(self, features: Dict) -> Dict:
        summary = {
            "avg_inter_meal_interval_hours": features.get('avg_inter_meal_interval_hours'),
            "longest_fasting_window_hours": features.get('longest_fasting_window_hours'),
            "meal_time_variance_seconds": features.get('meal_time_variance_seconds'),
            "num_dense_eating_periods": features.get('num_dense_eating_periods'),
        }
        return {k: v for k, v in summary.items() if v is not None}

    def _detect_patterns(self, features: Dict) -> list:
        patterns = []

        if features.get('longest_fasting_window_hours', 0) > 16: # Example threshold
            patterns.append("Long fasting window detected.")

        if features.get('num_dense_eating_periods', 0) > 5: # Example threshold
            patterns.append("High number of dense eating periods detected.")

        return patterns
