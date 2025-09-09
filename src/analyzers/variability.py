from typing import Dict, Any
from .base import BaseAnalyzer
from ..analysis_models.results import VariabilityAnalysisResult, PatternDetection

class VariabilityAnalyzer(BaseAnalyzer):
    """
    Analyzer for variability features.
    """
    def analyze(self) -> VariabilityAnalysisResult:
        features = self.data

        summary = self._summarize_variability(features)
        patterns = self._detect_patterns(features)

        return VariabilityAnalysisResult(
            summary=summary,
            patterns=PatternDetection(patterns=patterns, anomalies=[]),
            metadata=self.get_metadata()
        )

    def _summarize_variability(self, features: Dict) -> Dict:
        summary = {}
        for metric, data in features.items():
            summary[metric] = {
                "rolling_variance": data.get('rolling_variance'),
                "rolling_range": data.get('rolling_range'),
                "absolute_energy": data.get('absolute_energy'),
                "zero_crossing_rate": data.get('zero_crossing_rate'),
            }
        return summary

    def _detect_patterns(self, features: Dict) -> list:
        patterns = []

        hr_variability = features.get('heart_rate', {})
        if hr_variability.get('rolling_variance', 0) > 100: # Example threshold
            patterns.append("High heart rate variability detected.")

        steps_variability = features.get('steps', {})
        if steps_variability.get('zero_crossing_rate', 0) > 0.5: # Example threshold
            patterns.append("High noisiness in step count detected.")

        return patterns
