from typing import Dict, Any
from .base import BaseAnalyzer
from ..analysis_models.results import ActivityAnalysisResult, PatternDetection

class ActivityAnalyzer(BaseAnalyzer):
    """
    Analyzer for activity features.
    """
    def analyze(self) -> ActivityAnalysisResult:
        features = self.data

        summary = self._summarize_activity(features)
        patterns = self._detect_patterns(features)

        return ActivityAnalysisResult(
            summary=summary,
            patterns=PatternDetection(patterns=patterns, anomalies=[]),
            metadata=self.get_metadata()
        )

    def _summarize_activity(self, features: Dict) -> Dict:
        summary = {
            "average_cadence": features.get('average_cadence'),
            "average_pace_mps": features.get('average_pace_mps'),
            "num_activity_bursts": features.get('num_activity_bursts'),
            "avg_burst_duration_seconds": features.get('avg_burst_duration_seconds'),
            "num_rest_periods": features.get('num_rest_periods'),
        }
        return {k: v for k, v in summary.items() if v is not None}

    def _detect_patterns(self, features: Dict) -> list:
        patterns = []

        if features.get('num_activity_bursts', 0) > 10: # Example threshold
            patterns.append("High number of activity bursts detected.")

        if features.get('average_cadence', 0) > 120: # Example threshold
            patterns.append("High average cadence detected, suggesting intense activity.")

        return patterns
