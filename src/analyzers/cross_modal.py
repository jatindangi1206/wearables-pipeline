from typing import List, Dict, Any, Callable, Type
from src.analysis_models.results import (
    PhysiologicalAnalysisResult,
    MealAnalysisResult,
    LungFunctionAnalysisResult,
    CrossModalAnalysisResult,
    CrossModalPattern,
)
from datetime import datetime
from collections import defaultdict

class CrossModalPatternDetectorRegistry:
    _detectors: List[Callable] = []

    @classmethod
    def register(cls, detector: Callable):
        cls._detectors.append(detector)
        return detector

    @classmethod
    def get_detectors(cls):
        return cls._detectors

class CrossModalAnalyzer:
    def __init__(
        self,
        physiological: PhysiologicalAnalysisResult,
        meal: MealAnalysisResult,
        lung_function: LungFunctionAnalysisResult,
        circadian: "CircadianAnalysisResult" = None,
    ):
        self.physiological = physiological
        self.meal = meal
        self.lung_function = lung_function
        self.circadian = circadian

    def align_by_date(self) -> List[Dict[str, Any]]:
        # Aggregate all records by date (YYYY-MM-DD)
        date_map = defaultdict(dict)

        # Physiological: flatten stats by date if possible
        # For simplicity, use metadata or skip if not available
        # (Extend as needed for more granular alignment)
        # Here, we just add the stats as a block
        date_map["physiological"]["stats"] = self.physiological.stats
        date_map["physiological"]["patterns"] = self.physiological.patterns.patterns

        # Meals: group by date
        for day in self.meal.daily_summaries:
            date_map[day.date]["meals"] = [m.dict() for m in day.meals]
            date_map[day.date]["meal_count"] = day.meal_count

        # Lung function: group by date
        for entry in self.lung_function.entries:
            if entry.timestamp:
                date = entry.timestamp[:10]
                if "lung_function" not in date_map[date]:
                    date_map[date]["lung_function"] = []
                date_map[date]["lung_function"].append(entry.dict())

        # Flatten to list of dicts
        aligned = []
        for date, data in date_map.items():
            rec = {"date": date}
            rec.update(data)
            aligned.append(rec)
        aligned.sort(key=lambda x: x["date"])
        return aligned

    def detect_patterns(self, aligned_records: List[Dict[str, Any]]) -> List[CrossModalPattern]:
        patterns = []
        for detector in CrossModalPatternDetectorRegistry.get_detectors():
            patterns.extend(detector(self, aligned_records))
        return patterns

    def analyze(self) -> CrossModalAnalysisResult:
        aligned_records = self.align_by_date()
        detected_patterns = self.detect_patterns(aligned_records)
        metadata = {
            "analyzer": "CrossModalAnalyzer",
            "num_dates": len(aligned_records),
        }
        return CrossModalAnalysisResult(
            version="1.0",
            physiological=self.physiological,
            meal=self.meal,
            lung_function=self.lung_function,
            circadian=self.circadian,
            aligned_records=aligned_records,
            detected_patterns=detected_patterns,
            metadata=metadata,
        )

# --- Example pattern detectors ---

@CrossModalPatternDetectorRegistry.register
def meal_sleep_pattern(analyzer: CrossModalAnalyzer, aligned_records: List[Dict[str, Any]]) -> List[CrossModalPattern]:
    patterns = []
    for rec in aligned_records:
        meals = rec.get("meals", [])
        phys_patterns = rec.get("physiological", {}).get("patterns", [])
        if meals and any("sleep" in p.lower() for p in phys_patterns):
            patterns.append(CrossModalPattern(
                name="Meal-Sleep Correlation",
                description="Detected possible correlation between meal timing and sleep quality.",
                evidence={"date": rec["date"], "meals": meals, "phys_patterns": phys_patterns}
            ))
    return patterns

@CrossModalPatternDetectorRegistry.register
def hr_spo2_post_meal_pattern(analyzer: CrossModalAnalyzer, aligned_records: List[Dict[str, Any]]) -> List[CrossModalPattern]:
    patterns = []
    # Example: look for HR/SpO2 changes after meals (simplified)
    for rec in aligned_records:
        meals = rec.get("meals", [])
        phys_stats = rec.get("physiological", {}).get("stats", {})
        if meals and "heartrate" in phys_stats and "spo2" in phys_stats:
            hr_mean = phys_stats["heartrate"].mean
            spo2_mean = phys_stats["spo2"].mean
            if hr_mean and spo2_mean and hr_mean > 90 and spo2_mean < 95:
                patterns.append(CrossModalPattern(
                    name="HR/SpO2 Change Post-Meal",
                    description="Elevated HR and reduced SpO₂ detected after meals.",
                    evidence={"date": rec["date"], "hr_mean": hr_mean, "spo2_mean": spo2_mean}
                ))
    return patterns

@CrossModalPatternDetectorRegistry.register
def lung_function_vs_activity_pattern(analyzer: CrossModalAnalyzer, aligned_records: List[Dict[str, Any]]) -> List[CrossModalPattern]:
    patterns = []
    for rec in aligned_records:
        lung_entries = rec.get("lung_function", [])
        phys_stats = rec.get("physiological", {}).get("stats", {})
        if lung_entries and "steps" in phys_stats:
            steps_mean = phys_stats["steps"].mean
            for entry in lung_entries:
                fev1 = entry.get("fev1")
                if fev1 is not None and steps_mean is not None and steps_mean > 5000 and fev1 < 2.0:
                    patterns.append(CrossModalPattern(
                        name="Low Lung Function with High Activity",
                        description="Low FEV1 detected on high-activity day.",
                        evidence={"date": rec["date"], "steps_mean": steps_mean, "fev1": fev1}
                    ))
    return patterns