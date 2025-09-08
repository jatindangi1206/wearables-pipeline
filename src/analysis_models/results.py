from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class StatSummary(BaseModel):
    mean: Optional[float]
    median: Optional[float]
    mode: Optional[float]
    stddev: Optional[float]
    outliers: Optional[List[float]] = None

class CorrelationMatrix(BaseModel):
    matrix: Dict[str, Dict[str, Optional[float]]]

class ClinicalAssessment(BaseModel):
    status: str
    details: Optional[str] = None
    recommendations: Optional[List[str]] = None

class PatternDetection(BaseModel):
    patterns: List[str]
    anomalies: Optional[List[str]] = None

class PhysiologicalAnalysisResult(BaseModel):
    stats: Dict[str, StatSummary]
    correlations: CorrelationMatrix
    clinical_flags: Dict[str, ClinicalAssessment]
    patterns: PatternDetection
    metadata: Dict[str, Any]

class MealEntry(BaseModel):
    timestamp: str
    dish: str
    rating: Optional[float] = None
    customizations: Optional[List[str]] = None

class MealDaySummary(BaseModel):
    date: str
    meals: List[MealEntry]
    meal_count: int
    rating_distribution: Dict[str, int]

class MealAnalysisResult(BaseModel):
    daily_summaries: List[MealDaySummary]
    overall_patterns: PatternDetection
    metadata: Dict[str, Any]

class LungFunctionEntry(BaseModel):
    timestamp: str
    fev1: float
    fvc: float
    fev1_fvc: float

class LungFunctionAssessment(BaseModel):
    status: str
    reference_range: Optional[str] = None
    interpretation: Optional[str] = None
    recommendations: Optional[List[str]] = None

class LungFunctionAnalysisResult(BaseModel):
    entries: List[LungFunctionEntry]
    assessments: List[LungFunctionAssessment]
    metadata: Dict[str, Any]

# --- Cross-modal analysis result model ---

class CrossModalPattern(BaseModel):
    name: str
    description: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None

class CrossModalAnalysisResult(BaseModel):
    version: str = "1.0"
    physiological: PhysiologicalAnalysisResult
    meal: MealAnalysisResult
    lung_function: LungFunctionAnalysisResult
    aligned_records: List[Dict[str, Any]]  # temporally aligned/aggregated data
    detected_patterns: List[CrossModalPattern]
    metadata: Dict[str, Any]