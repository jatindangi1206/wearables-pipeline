from typing import Dict, Any
from .base import BaseAnalyzer
from ..analysis_models.results import SleepAnalysisResult, PatternDetection

class SleepAnalyzer(BaseAnalyzer):
    """
    Analyzer for sleep features.
    """
    def analyze(self) -> SleepAnalysisResult:
        features = self.data

        summary = self._summarize_sleep(features)
        patterns = self._detect_patterns(features)

        return SleepAnalysisResult(
            summary=summary,
            patterns=PatternDetection(patterns=patterns, anomalies=[]),
            metadata=self.get_metadata()
        )

    def _summarize_sleep(self, features: Dict) -> Dict:
        summary = {}
        sleep_dynamics = features.get('sleep_hr_dynamics', {})
        if sleep_dynamics:
            # Average the features across all sleep sessions
            avg_time_to_lowest_hr = None
            avg_onset_slope = None
            avg_wake_slope = None

            all_times = [v.get('time_to_lowest_hr_seconds') for v in sleep_dynamics.values() if v.get('time_to_lowest_hr_seconds') is not None]
            if all_times:
                avg_time_to_lowest_hr = sum(all_times) / len(all_times)

            all_onset_slopes = [v.get('hr_onset_slope') for v in sleep_dynamics.values() if v.get('hr_onset_slope') is not None]
            if all_onset_slopes:
                avg_onset_slope = sum(all_onset_slopes) / len(all_onset_slopes)

            all_wake_slopes = [v.get('hr_wake_slope') for v in sleep_dynamics.values() if v.get('hr_wake_slope') is not None]
            if all_wake_slopes:
                avg_wake_slope = sum(all_wake_slopes) / len(all_wake_slopes)

            summary = {
                "avg_time_to_lowest_hr_seconds": avg_time_to_lowest_hr,
                "avg_hr_onset_slope": avg_onset_slope,
                "avg_hr_wake_slope": avg_wake_slope,
            }
        return summary

    def _detect_patterns(self, features: Dict) -> list:
        patterns = []

        sleep_dynamics = features.get('sleep_hr_dynamics', {})
        if sleep_dynamics:
            avg_onset_slope = self._summarize_sleep(features).get('avg_hr_onset_slope')
            if avg_onset_slope and avg_onset_slope > 0:
                patterns.append("Heart rate tends to increase after sleep onset.")

        return patterns
