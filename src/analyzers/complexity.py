from typing import Dict, Any
from .base import BaseAnalyzer
from ..analysis_models.results import ComplexityAnalysisResult, PatternDetection

class ComplexityAnalyzer(BaseAnalyzer):
    """
    Analyzer for complexity features.
    """
    def analyze(self) -> ComplexityAnalysisResult:
        features = self.data

        summary = self._summarize_complexity(features)
        patterns = self._detect_patterns(features)

        return ComplexityAnalysisResult(
            summary=summary,
            patterns=PatternDetection(patterns=patterns, anomalies=[]),
            metadata=self.get_metadata()
        )

    def _summarize_complexity(self, features: Dict) -> Dict:
        summary = {}
        for metric, data in features.items():
            summary[metric] = {
                "approximate_entropy": data.get('approximate_entropy'),
                "sample_entropy": data.get('sample_entropy'),
            }
        return summary

    def _detect_patterns(self, features: Dict) -> list:
        patterns = []

        hr_complexity = features.get('heart_rate', {})
        if hr_complexity.get('sample_entropy', 0) < 0.1: # Example threshold
            patterns.append("Low sample entropy in heart rate detected, suggesting low complexity.")

        spo2_complexity = features.get('spo2_value', {})
        if spo2_complexity.get('sample_entropy', 0) < 0.05: # Example threshold
            patterns.append("Low sample entropy in SpO2 detected, suggesting low complexity.")

        return patterns
