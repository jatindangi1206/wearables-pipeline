import sys
from src.pipeline import PipelineOrchestrator
from src.ingestion import ingest_data
from src.utils.validation import validate_data
from src.analyzers.lung_function import LungFunctionAnalyzer
from src.analyzers.meal import MealAnalyzer
from src.analyzers.physiological import PhysiologicalAnalyzer
from src.analyzers.cross_modal import CrossModalAnalyzer
from src.reporting.report_generator import ReportGenerator
from src.features.circadian import CircadianFeaturesExtractor
from src.analyzers.circadian import CircadianAnalyzer
from src.features.variability import VariabilityFeaturesExtractor
from src.analyzers.variability import VariabilityAnalyzer
from src.features.complexity import ComplexityFeaturesExtractor
from src.analyzers.complexity import ComplexityAnalyzer
from src.features.sleep import SleepFeaturesExtractor
from src.analyzers.sleep import SleepAnalyzer
from src.features.activity import ActivityFeaturesExtractor
from src.analyzers.activity import ActivityAnalyzer
from src.features.temperature import TemperatureFeaturesExtractor
from src.analyzers.temperature import TemperatureAnalyzer
from src.features.meal import MealFeaturesExtractor
from src.analyzers.meal_features import MealFeaturesAnalyzer

def cleaning_fn(data):
    # No-op: data is already validated/model instances
    return data

def main(config_path):
    # Ingest data
    ingestion_fn = lambda: ingest_data(config_path)
    # Cleaning
    # (already defined as cleaning_fn)

    # Feature Extraction functions
    feature_extraction_fns = {
        'circadian': lambda d: CircadianFeaturesExtractor(d).extract_features(),
        'variability': lambda d: VariabilityFeaturesExtractor(d).extract_features(),
        'complexity': lambda d: ComplexityFeaturesExtractor(d).extract_features(),
        'sleep': lambda d: SleepFeaturesExtractor(d).extract_features(),
        'activity': lambda d: ActivityFeaturesExtractor(d).extract_features(),
        'temperature': lambda d: TemperatureFeaturesExtractor(d).extract_features(),
        'meal': lambda d: MealFeaturesExtractor(d).extract_features(),
    }

    # Analysis functions
    def lung_fn(data):
        lung_dicts = []
        for d in data['lung_function']:
            dct = d.model_dump() if hasattr(d, "model_dump") else (d.dict() if hasattr(d, "dict") else vars(d))
            # Filter out records missing required fields
            if all(dct.get(k) is not None for k in ("fev1", "fvc", "fev1_fvc")):
                lung_dicts.append(dct)
        return LungFunctionAnalyzer(lung_dicts).analyze()
    def meal_fn(data):
        meal_dicts = []
        for d in data['meal']:
            dct = d.model_dump() if hasattr(d, "model_dump") else (d.dict() if hasattr(d, "dict") else vars(d))
            if dct.get("time") is not None:
                meal_dicts.append(dct)
        return MealAnalyzer(meal_dicts).analyze()
    def physio_fn(data):
        physio_records = []
        for k in ['blood_pressure', 'heart_rate', 'sleep', 'spo2', 'steps', 'temperature']:
            for d in data[k]:
                dct = d.model_dump() if hasattr(d, "model_dump") else (d.dict() if hasattr(d, "dict") else vars(d))
                if dct.get("created_time") is not None or dct.get("log_date_time") is not None:
                    physio_records.append(dct)
        return PhysiologicalAnalyzer(physio_records).analyze()
    def circadian_fn(data):
        circadian_features = data.get('features', {}).get('circadian', {})
        return CircadianAnalyzer(circadian_features).analyze()
    def variability_fn(data):
        variability_features = data.get('features', {}).get('variability', {})
        return VariabilityAnalyzer(variability_features).analyze()
    def complexity_fn(data):
        complexity_features = data.get('features', {}).get('complexity', {})
        return ComplexityAnalyzer(complexity_features).analyze()
    def sleep_analysis_fn(data):
        sleep_features = data.get('features', {}).get('sleep', {})
        return SleepAnalyzer(sleep_features).analyze()
    def activity_analysis_fn(data):
        activity_features = data.get('features', {}).get('activity', {})
        return ActivityAnalyzer(activity_features).analyze()
    def temperature_analysis_fn(data):
        temperature_features = data.get('features', {}).get('temperature', {})
        return TemperatureAnalyzer(temperature_features).analyze()
    def meal_features_analysis_fn(data):
        meal_features = data.get('features', {}).get('meal', {})
        return MealFeaturesAnalyzer(meal_features).analyze()

    analysis_fns = {
        'lung_function': lung_fn,
        'meal': meal_fn,
        'physiological': physio_fn,
        'circadian': circadian_fn,
        'variability': variability_fn,
        'complexity': complexity_fn,
        'sleep': sleep_analysis_fn,
        'activity': activity_analysis_fn,
        'temperature': temperature_analysis_fn,
        'meal_features': meal_features_analysis_fn,
    }
    # Cross-modal
    from src.analysis_models.results import MealAnalysisResult, LungFunctionAnalysisResult, PatternDetection
    cross_modal_fn = lambda results: CrossModalAnalyzer(
        results["physiological"],
        results["meal"],
        results["lung_function"],
        results.get("circadian"),
        results.get("variability"),
        results.get("complexity"),
        results.get("sleep"),
        results.get("activity"),
        results.get("temperature"),
        results.get("meal_features")
    ).analyze()
    # Reporting
    report_fn = lambda cross_modal_result: ReportGenerator().generate_report(cross_modal_result)

    orchestrator = PipelineOrchestrator(
        ingestion_fn=ingestion_fn,
        cleaning_fn=cleaning_fn,
        feature_extraction_fns=feature_extraction_fns,
        analysis_fns=analysis_fns,
        cross_modal_fn=cross_modal_fn,
        report_fn=report_fn
    )

    try:
        results = orchestrator.run()
        print("Pipeline completed successfully.")
        print("Report Output:")
        print(results.get('report'))
    except Exception as e:
        print("Pipeline failed:", e)
        sys.exit(1)

if __name__ == "__main__":
    config_path = "config.yaml"
    main(config_path)