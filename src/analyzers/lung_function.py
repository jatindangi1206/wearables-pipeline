from typing import List, Dict, Any
from src.analyzers.base import BaseAnalyzer
from src.clinical import reference_ranges as ref
from src.analysis_models.results import (
    LungFunctionEntry, LungFunctionAssessment, LungFunctionAnalysisResult
)

class LungFunctionAnalyzer(BaseAnalyzer):
    """
    Analyzer for lung function data: FEV1, FEV1/FVC, reference comparison.
    """

    def analyze(self, age: int = None, gender: str = None) -> LungFunctionAnalysisResult:
        entries = []
        assessments = []

        for d in self.data:
            fev1 = d.get("fev1")
            fvc = d.get("fvc")
            fev1_fvc = d.get("fev1_fvc")
            timestamp = d.get("timestamp")

            ts_str = None
            if timestamp:
                ts_str = timestamp.isoformat()

            entries.append(LungFunctionEntry(
                timestamp=ts_str,
                fev1=fev1,
                fvc=fvc,
                fev1_fvc=fev1_fvc
            ))

            # Reference comparison
            status = "unknown"
            interpretation = ""
            recommendations = []
            ref_range = None

            if age is not None and gender is not None:
                fev1_range = ref.get_fev1_range(age, gender)
                fev1_fvc_range = ref.get_fev1_fvc_range(gender)
                if fev1_range:
                    ref_range = f"{fev1_range[0]} - {fev1_range[1]}"
                    if fev1 < fev1_range[0]:
                        status = "reduced"
                        interpretation = "FEV1 below reference range"
                        recommendations.append("Possible airway obstruction")
                    else:
                        status = "normal"
                        interpretation = "FEV1 within reference range"
                if fev1_fvc_range:
                    if fev1_fvc < fev1_fvc_range[0]:
                        status = "obstructive"
                        interpretation += "; FEV1/FVC below normal"
                        recommendations.append("Consider COPD/asthma assessment")
            else:
                status = "reference_unavailable"
                interpretation = "No age/gender provided for reference"

            assessments.append(LungFunctionAssessment(
                status=status,
                reference_range=ref_range,
                interpretation=interpretation,
                recommendations=recommendations if recommendations else None
            ))

        return LungFunctionAnalysisResult(
            entries=entries,
            assessments=assessments,
            metadata=self.get_metadata()
        )