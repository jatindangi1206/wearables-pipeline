from typing import Any, Dict
from src.analysis_models.results import CrossModalAnalysisResult
import json
import os

class ReportGenerator:
    def __init__(self, output_format: str = "json"):
        self.output_format = output_format.lower()
        if self.output_format not in {"json"}:
            raise ValueError(f"Unsupported format: {self.output_format}")

    def generate_report(self, result: CrossModalAnalysisResult) -> Dict[str, Any]:
        report = {
            "version": result.version,
            "summary": self._summarize_key_findings(result),
            "detected_patterns": self._extract_patterns(result),
            "clinical_flags": self._extract_clinical_flags(result),
            "metadata": result.metadata,
        }
        return report

    def save_report(self, result: CrossModalAnalysisResult, output_path: str) -> None:
        report = self.generate_report(result)
        if self.output_format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

    def _summarize_key_findings(self, result: CrossModalAnalysisResult) -> Dict[str, Any]:
        summary = {}

        # Physiological summary
        phys = result.physiological
        summary["physiological"] = {
            "stats": {k: v.dict() for k, v in phys.stats.items()},
            "notable_correlations": self._extract_notable_correlations(phys.correlations.matrix),
            "patterns": phys.patterns.patterns,
        }

        # Meal summary
        meal = result.meal
        summary["meal"] = {
            "overall_patterns": meal.overall_patterns.patterns,
            "days_analyzed": len(meal.daily_summaries),
            "rating_distribution": self._aggregate_meal_ratings(meal),
        }

        # Lung function summary
        lung = result.lung_function
        summary["lung_function"] = {
            "entry_count": len(lung.entries),
            "assessment_statuses": [a.status for a in getattr(lung, "assessments", [])],
        }

        # Cross-modal patterns
        summary["cross_modal_patterns"] = [
            {"name": p.name, "description": p.description} for p in result.detected_patterns
        ]

        return summary

    def _extract_patterns(self, result: CrossModalAnalysisResult) -> Any:
        return [
            {
                "name": p.name,
                "description": p.description,
                "evidence": p.evidence,
            }
            for p in result.detected_patterns
        ]

    def _extract_clinical_flags(self, result: CrossModalAnalysisResult) -> Dict[str, Any]:
        flags = {}
        # Physiological clinical flags
        flags["physiological"] = {
            k: v.dict() for k, v in result.physiological.clinical_flags.items()
        }
        # Lung function assessments (if present)
        lung = result.lung_function
        if hasattr(lung, "assessments"):
            flags["lung_function"] = [a.dict() for a in lung.assessments]
        return flags

    def _extract_notable_correlations(self, matrix: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        notable = {}
        for var1, row in matrix.items():
            for var2, value in row.items():
                if value is not None and abs(value) > 0.7 and var1 != var2:
                    key = f"{var1}-{var2}"
                    notable[key] = value
        return notable

    def _aggregate_meal_ratings(self, meal) -> Dict[str, int]:
        # Aggregate all rating distributions across days
        agg = {}
        for day in meal.daily_summaries:
            for rating, count in day.rating_distribution.items():
                agg[rating] = agg.get(rating, 0) + count
        return agg
