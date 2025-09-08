import sys
from src.pipeline import PipelineOrchestrator
from src.ingestion import ingest_data
from src.utils.validation import validate_data
from src.analyzers.lung_function import LungFunctionAnalyzer
from src.analyzers.meal import MealAnalyzer
from src.analyzers.physiological import PhysiologicalAnalyzer
from src.analyzers.cross_modal import CrossModalAnalyzer
from src.reporting.report_generator import ReportGenerator

def cleaning_fn(data):
    # No-op: data is already validated/model instances
    return data

def main(config_path):
    # Ingest data
    ingestion_fn = lambda: ingest_data(config_path)
    # Cleaning
    # (already defined as cleaning_fn)
    # Analysis functions
    def lung_fn(data):
        lung_dicts = []
        for d in data['lung_function']:
            dct = d.model_dump() if hasattr(d, "model_dump") else (d.dict() if hasattr(d, "dict") else vars(d))
            # Filter out records missing required fields
            if all(dct.get(k) is not None for k in ("fev1", "fvc", "fev1_fvc", "timestamp")):
                lung_dicts.append(dct)
        return LungFunctionAnalyzer(lung_dicts).analyze()
    def meal_fn(data):
        meal_dicts = []
        for d in data['meal']:
            dct = d.model_dump() if hasattr(d, "model_dump") else (d.dict() if hasattr(d, "dict") else vars(d))
            if dct.get("timestamp") is not None:
                meal_dicts.append(dct)
        return MealAnalyzer(meal_dicts).analyze()
    def physio_fn(data):
        physio_records = []
        for k in ['blood_pressure', 'heart_rate', 'sleep', 'spo2', 'steps', 'temperature']:
            for d in data[k]:
                dct = d.model_dump() if hasattr(d, "model_dump") else (d.dict() if hasattr(d, "dict") else vars(d))
                if dct.get("timestamp") is not None:
                    physio_records.append(dct)
        return PhysiologicalAnalyzer(physio_records).analyze()
    analysis_fns = {
        'lung_function': lung_fn,
        'meal': meal_fn,
        'physiological': physio_fn
    }
    # Cross-modal
    from src.analysis_models.results import MealAnalysisResult, LungFunctionAnalysisResult, PatternDetection
    cross_modal_fn = lambda results: CrossModalAnalyzer(
        results["physiological"],
        results["meal"],
        results["lung_function"]
    ).analyze()
    # Reporting
    report_fn = lambda cross_modal_result: ReportGenerator().generate_report(cross_modal_result)

    orchestrator = PipelineOrchestrator(
        ingestion_fn=ingestion_fn,
        cleaning_fn=cleaning_fn,
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