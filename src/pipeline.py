from enum import Enum, auto


class PipelineState(Enum):
    NOT_STARTED = auto()
    INGESTION = auto()
    CLEANING = auto()
    ANALYSIS = auto()
    CROSS_MODAL_ANALYSIS = auto()
    REPORT_GENERATION = auto()
    COMPLETED = auto()
    ERROR = auto()


class PipelineOrchestrator:
    def __init__(self, ingestion_fn, cleaning_fn, analysis_fns, cross_modal_fn, report_fn):
        self.state = PipelineState.NOT_STARTED
        self.error = None
        self.ingestion_fn = ingestion_fn
        self.cleaning_fn = cleaning_fn
        self.analysis_fns = analysis_fns  # List of callables for individual analyses
        self.cross_modal_fn = cross_modal_fn
        self.report_fn = report_fn
        self.results = {}

    def run(self, *args, **kwargs):
        try:
            self._transition(PipelineState.INGESTION)
            data = self.ingestion_fn(*args, **kwargs)
            self.results['ingested'] = data

            self._transition(PipelineState.CLEANING)
            cleaned = self.cleaning_fn(data)
            self.results['cleaned'] = cleaned

            self._transition(PipelineState.ANALYSIS)
            analysis_results = {}
            for name, fn in self.analysis_fns.items():
                analysis_results[name] = fn(cleaned)
            self.results['analysis'] = analysis_results

            self._transition(PipelineState.CROSS_MODAL_ANALYSIS)
            cross_modal_result = self.cross_modal_fn(analysis_results)
            self.results['cross_modal'] = cross_modal_result

            self._transition(PipelineState.REPORT_GENERATION)
            report = self.report_fn(cross_modal_result)
            self.results['report'] = report

            self._transition(PipelineState.COMPLETED)
            return self.results

        except Exception as e:
            self.error = e
            self._transition(PipelineState.ERROR)
            raise

    def _transition(self, new_state):
        # Enforce valid transitions if needed
        self.state = new_state

    def get_state(self):
        return self.state

    def get_error(self):
        return self.error

    def extend_stage(self, stage_name, fn):
        # Allow adding new stages dynamically
        setattr(self, stage_name, fn)