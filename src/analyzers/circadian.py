from typing import Dict, Any
from .base import BaseAnalyzer
from ..analysis_models.results import CircadianAnalysisResult, PatternDetection

class CircadianAnalyzer(BaseAnalyzer):
    """
    Analyzer for circadian features.
    """
    def analyze(self) -> CircadianAnalysisResult:
        features = self.data # The data passed to the analyzer is the extracted features dict

        summary = {
            "time_segment_summary": self._summarize_time_segments(features.get('time_segment_avg', {})),
            "weekday_weekend_summary": self._summarize_weekday_weekend(features.get('weekday_vs_weekend', {}))
        }

        patterns = self._detect_patterns(features)

        return CircadianAnalysisResult(
            summary=summary,
            patterns=PatternDetection(patterns=patterns, anomalies=[]),
            metadata=self.get_metadata()
        )

    def _summarize_time_segments(self, time_segment_avg: Dict) -> Dict:
        summary = {}
        for segment, metrics in time_segment_avg.items():
            summary[segment] = {
                "avg_heart_rate": metrics.get('heart_rate'),
                "avg_spo2": metrics.get('spo2_value'),
            }
        return summary

    def _summarize_weekday_weekend(self, weekday_weekend_avg: Dict) -> Dict:
        summary = {}
        for day_type, metrics in weekday_weekend_avg.items():
            summary[day_type] = {
                "avg_steps": metrics.get('steps'),
                "avg_heart_rate": metrics.get('heart_rate'),
            }
        return summary

    def _detect_patterns(self, features: Dict) -> list:
        patterns = []

        time_segment_avg = features.get('time_segment_avg', {})
        night_hr = time_segment_avg.get('night', {}).get('heart_rate')
        morning_hr = time_segment_avg.get('morning', {}).get('heart_rate')
        if night_hr and morning_hr and night_hr > morning_hr:
            patterns.append("Elevated heart rate during the night compared to the morning.")

        weekday_vs_weekend = features.get('weekday_vs_weekend', {})
        weekday_steps = weekday_vs_weekend.get('weekday_avg', {}).get('steps')
        weekend_steps = weekday_vs_weekend.get('weekend_avg', {}).get('steps')
        if weekday_steps and weekend_steps and weekend_steps > weekday_steps * 1.5:
            patterns.append("Significantly higher activity levels on weekends.")

        return patterns
