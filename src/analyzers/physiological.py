from typing import List, Dict, Any
from src.analyzers.base import BaseAnalyzer
from src.stats import utils as stat_utils
from src.clinical import reference_ranges as ref
from src.analysis_models.results import (
    StatSummary, CorrelationMatrix, ClinicalAssessment,
    PatternDetection, PhysiologicalAnalysisResult
)

class PhysiologicalAnalyzer(BaseAnalyzer):
    """
    Analyzer for physiological data: BP, HR, SpO2, Steps, Sleep, Temperature.
    """

    def analyze(self) -> PhysiologicalAnalysisResult:
        stats = {}
        clinical_flags = {}
        patterns = []
        anomalies = []

        # Extract metrics
        metrics = {
            "systolic": [d.get("systolic") for d in self.data if d.get("systolic") is not None],
            "diastolic": [d.get("diastolic") for d in self.data if d.get("diastolic") is not None],
            "heartrate": [d.get("heartrate") for d in self.data if d.get("heartrate") is not None],
            "spo2": [d.get("spo2") for d in self.data if d.get("spo2") is not None],
            "steps": [d.get("steps") for d in self.data if d.get("steps") is not None],
            "temperature": [d.get("temperature") for d in self.data if d.get("temperature") is not None],
            "sleep_stage_deep": [d.get("sleep_stage_deep") for d in self.data if d.get("sleep_stage_deep") is not None],
            "sleep_stage_rem": [d.get("sleep_stage_rem") for d in self.data if d.get("sleep_stage_rem") is not None],
            "sleep_stage_light": [d.get("sleep_stage_light") for d in self.data if d.get("sleep_stage_light") is not None],
        }

        # Baseline statistics
        for metric, values in metrics.items():
            stats[metric] = StatSummary(
                mean=stat_utils.mean(values),
                median=stat_utils.median(values),
                mode=stat_utils.mode(values),
                stddev=stat_utils.stddev(values),
                outliers=stat_utils.detect_outliers(values)
            )

        # Correlation matrix for selected metrics
        corr_metrics = {k: v for k, v in metrics.items() if k in ["systolic", "diastolic", "heartrate", "spo2", "steps", "temperature"]}
        correlations = CorrelationMatrix(matrix=stat_utils.correlation_matrix(corr_metrics))

        # Clinical threshold analysis
        # Heart Rate
        hr_vals = metrics["heartrate"]
        if hr_vals:
            if any(hr > 100 for hr in hr_vals):
                hr_flag = ClinicalAssessment(status="tachycardia", details="Resting HR > 100 bpm", recommendations=["Consult physician"])
            elif any(hr < 60 for hr in hr_vals):
                hr_flag = ClinicalAssessment(status="bradycardia", details="Resting HR < 60 bpm", recommendations=["Monitor for symptoms"])
            else:
                hr_flag = ClinicalAssessment(status="normal")
        else:
            hr_flag = ClinicalAssessment(status="unknown")
        clinical_flags["heartrate"] = hr_flag

        # SpO2
        spo2_vals = metrics["spo2"]
        if spo2_vals:
            if any(s < 90 for s in spo2_vals):
                spo2_flag = ClinicalAssessment(status="severe_hypoxemia", details="SpO2 < 90%", recommendations=["Immediate attention"])
            elif any(s < 95 for s in spo2_vals):
                spo2_flag = ClinicalAssessment(status="mild_hypoxemia", details="SpO2 < 95%", recommendations=["Monitor closely"])
            else:
                spo2_flag = ClinicalAssessment(status="normal")
        else:
            spo2_flag = ClinicalAssessment(status="unknown")
        clinical_flags["spo2"] = spo2_flag

        # Temperature
        temp_vals = metrics["temperature"]
        if temp_vals:
            if any(t > 37.2 for t in temp_vals):
                temp_flag = ClinicalAssessment(status="fever", details="Temperature > 37.2°C", recommendations=["Hydrate, rest, monitor"])
            elif any(t < 36.0 for t in temp_vals):
                temp_flag = ClinicalAssessment(status="hypothermia", details="Temperature < 36.0°C", recommendations=["Warmth, monitor"])
            else:
                temp_flag = ClinicalAssessment(status="normal")
        else:
            temp_flag = ClinicalAssessment(status="unknown")
        clinical_flags["temperature"] = temp_flag

        # Pattern detection (simple examples)
        if hr_vals and any(hr > 100 for hr in hr_vals):
            patterns.append("Elevated resting heart rate detected")
        if spo2_vals and any(s < 95 for s in spo2_vals):
            patterns.append("Low SpO2 detected at least once")
        if temp_vals and any(t > 37.2 for t in temp_vals):
            patterns.append("Fever pattern detected")

        # Outlier detection
        for metric, summary in stats.items():
            if summary.outliers:
                anomalies.append(f"Outliers in {metric}: {summary.outliers}")

        pattern_detection = PatternDetection(patterns=patterns, anomalies=anomalies)

        return PhysiologicalAnalysisResult(
            stats=stats,
            correlations=correlations,
            clinical_flags=clinical_flags,
            patterns=pattern_detection,
            metadata=self.get_metadata()
        )