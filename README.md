# Health Data Pipeline

A modular pipeline for ingesting, processing, analyzing, and reporting on physiological, meal, and lung function data from wearable devices and clinical sources.

---

## Project Structure

```
wearables-pipeline/
├── config.yaml                # Pipeline configuration
├── requirements.txt           # Python dependencies
├── run_pipeline.py            # Main entry point to run the pipeline
├── input/                     # Input data directory
│   ├── lungs_data/            # Raw lung function data (CSV)
│   ├── meals_data/            # Raw meal data (CSV)
│   └── physio_data/           # Raw physiological data (CSV/JSON)
├── src/
│   ├── ingestion.py           # Data ingestion logic
│   ├── pipeline.py            # Pipeline orchestration
│   ├── models/                # Data models
│   ├── processors/            # Data processors (CSV, JSON, specialized)
│   ├── analyzers/             # Analysis modules (physiological, meal, lung, cross-modal)
│   ├── clinical/              # Clinical reference ranges
│   ├── stats/                 # Statistical utilities
│   ├── utils/                 # Utility functions (validation, timestamps)
│   ├── analysis_models/       # Analysis result models
│   └── reporting/             # Report generation
└── tests/                     # Unit tests
```

---

## Pipeline Stages

1. **Ingestion**  
   [`src/ingestion.py`](src/ingestion.py): Loads raw data from the `input/` directory, supporting multiple formats (CSV, JSON).

2. **Processing**  
   [`src/processors/`](src/processors/): Cleans, validates, and standardizes data using format-specific and specialized processors.

3. **Analysis**  
   [`src/analyzers/`](src/analyzers/): Extracts insights from physiological, meal, and lung function data. Supports cross-modal analysis.

4. **Clinical Reference**  
   [`src/clinical/reference_ranges.py`](src/clinical/reference_ranges.py): Provides clinical thresholds for interpreting results.

5. **Statistical Utilities**  
   [`src/stats/utils.py`](src/stats/utils.py): Common statistical calculations used in analysis.

6. **Reporting**  
   [`src/reporting/report_generator.py`](src/reporting/report_generator.py): Generates summary reports from analysis results.

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <repo-url>
cd wearables-pipeline
```

### 2. Create a Virtual Environment

```sh
pwd  # Confirm you are in the project root
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Prepare Input Data

Place your data files in the appropriate subfolders under `input/`:
- `input/physio_data/` for physiological data (CSV/JSON)
- `input/meals_data/` for meal data (CSV)
- `input/lungs_data/` for lung function data (CSV)

---

## Running the Pipeline

```sh
python run_pipeline.py
```

- The pipeline reads configuration from [`config.yaml`](config.yaml).
- Output reports and logs will be generated as specified in the config or printed to the console.

---

## Interpreting Outputs

- **Reports:**  
  Generated reports summarize key metrics and clinical interpretations for each data type.
- **Logs:**  
  Console/log output provides details on each pipeline stage, including any data validation issues.
- **Intermediate Results:**  
  Analysis results are structured using models in [`src/analysis_models/results.py`](src/analysis_models/results.py).

---

## For Maintainers

- **Adding New Data Types:**  
  Implement new processors in [`src/processors/`](src/processors/) and analyzers in [`src/analyzers/`](src/analyzers/).
- **Testing:**  
  Run unit tests with:
  ```sh
  python -m unittest discover tests
  ```
- **Configuration:**  
  Update [`config.yaml`](config.yaml) to adjust pipeline behavior.

---

## Support

For questions or contributions, please open an issue or submit a pull request.
