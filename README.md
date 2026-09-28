# AIMLCZG549: API-driven Cloud Native Solutions
## Assignment I — Cloud-Based Data Science Pipeline & API-Driven Architecture
**Course:** API-driven Cloud Native Solutions (AIMLCZG549)  
**Programme:** BITS Pilani WILP (M.Tech AI/ML & Cloud Computing)  
**Evaluation:** Continuous Evaluation Component (EC-1) | **Weightage:** 15 Marks | **Group ID:** 80  

---

## 1. Group Details & Contribution Matrix (Group ID: 80)

| Student Name | Student ID | Specific Module & Contribution Description | Share % |
| :--- | :--- | :--- | :---: |
| **SREE TEJA R** | 2025AE05629 | Pipeline Architecture, Prefect DataOps Automation (1.5), Cloud-Native FastAPI Gateway (3.1–3.3) | 100% |
---

## 2. Deliverables & Submission Files

1. **`group80.docx` / `80.docx` / `AIMLCZG549_Assignment1_Report.docx`**: Complete Word Document containing project details, embedded application screenshots, statistical tables, and group contribution matrix. (Ready for direct portal upload as required by Submission Guideline a).
2. **`group80.pdf` / `80.pdf` / `AIMLCZG549_Assignment1_Report.pdf`**: Publication-quality 8-page formatted PDF report with high-resolution figures and screenshots. (Ready for direct portal upload as required by Submission Guideline a).
3. **`AIMLCZG549_Assignment1_DataOps.ipynb`**: Fully executed, self-contained Jupyter Notebook executing all steps from 1.1 to 3.3.
4. **`video_presentation_script.md`**: 5-minute video demonstration walkthrough script for recording the video presentation (Submission Guideline b).
5. **`figures/`**: 8 high-resolution publication-quality plots (univariate, bivariate, cohort binning, correlations, feature importance, architecture).
6. **`screenshots/`**: 5 authentic application screenshots (Prefect Cloud Dashboard, Swagger UI `/docs`, Postman API testing, Terminal execution, Negative status code testing).
7. **`test_results/`**: Automated API test logs, sample request/response JSON payloads, and status code verification summaries.

---

## 3. Directory Layout

```
AIMLCZG549_Assignment1/
├── AIMLCZG549_Assignment1_DataOps.ipynb # Fully executed Jupyter Notebook
├── AIMLCZG549_Assignment1_Report.docx  # Final Word Document submission
├── AIMLCZG549_Assignment1_Report.pdf   # Final PDF Report submission
├── video_presentation_script.md        # Walkthrough script for video recording
├── README.md                           # Project documentation
│
├── data/
│   ├── telco_customer_churn.csv        # Raw dataset (7,043 rows, 21 columns)
│   ├── processed_telco_churn.csv      # Cleaned, imputed, and normalized dataset
│   └── pipeline_metrics.json          # Live telemetry emitted by DataOps pipeline
│
├── figures/                            # Publication-quality evaluation plots
│   ├── dataops_pipeline_architecture.png
│   ├── churn_distribution.png
│   ├── numeric_distributions.png
│   ├── bivariate_contract_churn.png
│   ├── bivariate_charges_churn.png
│   ├── tenure_cohort_analysis.png
│   ├── correlation_heatmap.png
│   └── feature_importance_ranking.png
│
├── screenshots/                       # Application and API testing screenshots
│   ├── 01_prefect_cloud_dashboard.png
│   ├── 02_fastapi_swagger_docs.png
│   ├── 03_postman_api_testing.png
│   ├── 04_terminal_dataops_execution.png
│   └── 05_api_status_codes_verification.png
│
├── src/                               # Modular Python source code
│   ├── config.py                      # Paths, features, hyperparameters
│   ├── pipeline.py                    # Complete Prefect DataOps pipeline flow
│   ├── deployment.py                  # Prefect deployment with 2-minute schedule
│   ├── api_service.py                 # FastAPI microservice with Built-in API integration
│   ├── test_api.py                    # Automated test suite (200, 202, 404, 422)
│   ├── generate_notebook.py           # Jupyter Notebook generator
│   ├── generate_screenshots.py        # High-resolution screenshot renderer
│   ├── generate_docx_report.py        # Word Document report builder
│   └── generate_pdf_report.py         # WeasyPrint PDF report compiler
│
└── test_results/                      # Captured API payloads and verification logs
    ├── api_test_summary.json
    ├── sample_app_details_response.json
    ├── sample_deployment_response.json
    ├── sample_flow_response.json
    ├── sample_flow_runs_response.json
    └── sample_prediction_response.json
```

---

## 4. Quick Start & Execution Instructions

### A. Environment Activation
```bash
source .venv/bin/activate
export PYTHONPATH="/Users/sreeteja/javaT/ConversationalAnalytics:$PYTHONPATH"
export PREFECT_HOME="/Users/sreeteja/javaT/ConversationalAnalytics/AIMLCZG549_Assignment1/.prefect"
export PREFECT_SERVER_ANALYTICS_ENABLED="false"
export DO_NOT_TRACK="1"
```

### B. Execute the Prefect DataOps Pipeline
```bash
python AIMLCZG549_Assignment1/src/pipeline.py
```
*Executes Data Ingestion (7,043 rows), Preprocessing (missing imputation, normalization), EDA (correlations, binning, encoding, feature importance), and saves telemetry to `data/pipeline_metrics.json`.*

### C. Register and Serve the 2-Minute Scheduled Deployment
```bash
# Register deployment
python AIMLCZG549_Assignment1/src/deployment.py

# To run continuous 2-minute scheduler:
python AIMLCZG549_Assignment1/src/deployment.py --serve
```

### D. Run the Cloud-Native API Gateway (FastAPI)
```bash
uvicorn AIMLCZG549_Assignment1.src.api_service:app --host 127.0.0.1 --port 8000 --reload
```
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Key Application Details: `http://127.0.0.1:8000/api/v1/application/details`

### E. Run the Automated API Test Suite
```bash
python AIMLCZG549_Assignment1/src/test_api.py
```
*Validates 12 test cases verifying HTTP status codes 200, 202, 404, and 422.*

### F. Recompile Submission Documents
```bash
# Recompile Word Document (.docx)
python AIMLCZG549_Assignment1/src/generate_docx_report.py

# Recompile PDF Document (.pdf)
python AIMLCZG549_Assignment1/src/generate_pdf_report.py
```
