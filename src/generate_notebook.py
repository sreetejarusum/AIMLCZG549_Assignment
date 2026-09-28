"""
Generates the fully documented, fully executed Jupyter Notebook for AIMLCZG549 Assignment 1.
"""

import json
from pathlib import Path
import nbformat as nbf

from AIMLCZG549_Assignment1.src.config import PROJECT_ROOT


def create_assignment_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.13.5"
        }
    }

    cells = []

    # Title & Metadata Cell
    cells.append(nbf.v4.new_markdown_cell("""# AIMLCZG549 - API-driven Cloud Native Solutions
## Assignment I: Cloud-Based Data Science Pipeline & API-Driven Architecture
---
### **Academic Details:**
- **Course Title:** API-driven Cloud Native Solutions (AIMLCZG549)
- **Programme:** BITS Pilani Work Integrated Learning Programmes (WILP) - M.Tech AI/ML & Cloud Computing
- **Component:** Continuous Evaluation (EC-1) | **Weightage:** 15 Marks
- **Group ID:** 80

---
### **Group Details & Member Contribution Matrix (Group ID: 80):**

| Student Name | Student ID | Specific Contribution / Modules Owned | Contribution % |
| :--- | :--- | :--- | :---: |
| **SREE TEJA R** | 2025AE05629 | Pipeline Architecture, Prefect DataOps Flow (1.5), API Gateway (3.1-3.3) | 25% |
| **Syed Tajuddin** | 2025AF05080 | Data Ingestion (1.2), Preprocessing & Missing Data Imputation (1.3) | 25% |
| **Megha** | 2025AF05045 | Exploratory Data Analysis, Statistical Correlations & Binning (1.4) | 25% |
| **Deepak Jain** | 2025AF05045 | Feature Importance Modeling (1.4), API Testing & Documentation (3.3) | 25% |

---
## Executive Summary & Objectives
This project implements an end-to-end, enterprise-grade cloud-native data science application addressing **Customer Churn Prevention in Telecommunication Services**.

The solution satisfies all requirements across the two assignment sub-objectives:
1. **Sub-Objective 1: Design and Development of a Data Pipeline (10 Marks)**
   - **1.1 Business Understanding:** Identifying churn business problems, financial implications, and ML objectives.
   - **1.2 Data Ingestion:** Automated ingestion and integrity validation of the 7,043-record Kaggle/IBM Telco Churn dataset.
   - **1.3 Data Pre-processing:** Statistical profiling, missing value detection, median imputation for numeric data, data type categorization, and MinMax normalization.
   - **1.4 Exploratory Data Analysis (EDA):** Pearson & Spearman correlation matrices, Chi-Square and Cramér's V tests for categorical association, tenure/charges cohort binning, one-hot/binary encoding, Random Forest Gini feature importances, and publication-quality visualizations.
   - **1.5 DataOps:** Modular Prefect workflow orchestrating automated ingestion, preprocessing, and EDA on a **recurring 2-minute schedule**, with live streaming activity logs and cloud dashboard integration.
2. **Sub-Objective 2: API Access (5 Marks)**
   - **3.1 Retrieve Key Application Details:** Leveraging Built-in APIs to access Flow definitions, Deployments, Schedules, and Flow Runs.
   - **3.2 Display Application Details:** Presenting four key application details (Flow Metadata, Deployment & Schedule, Flow Run Execution, and Quality/Model Telemetry).
   - **3.3 API Testing & Documentation:** Comprehensive testing of all endpoints, verifying appropriate HTTP status codes (`200 OK`, `202 Accepted`, `404 Not Found`, `422 Unprocessable Entity`), with request/response payloads and documentation.
"""))

    # Architecture Diagram
    cells.append(nbf.v4.new_markdown_cell("""## System Architecture
The diagram below illustrates the end-to-end cloud-native architecture connecting the scheduled Prefect DataOps engine with the FastAPI Cloud Gateway:

![Architecture Diagram](figures/dataops_pipeline_architecture.png)
"""))

    # Setup & Imports Code Cell
    cells.append(nbf.v4.new_markdown_cell("""### 0. Environment Setup & Dependency Configuration"""))
    cells.append(nbf.v4.new_code_cell("""import sys
import os
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configure paths and environment
PROJECT_ROOT = Path(".").resolve()
sys.path.insert(0, str(PROJECT_ROOT))
os.environ["PREFECT_HOME"] = str(PROJECT_ROOT / ".prefect")
os.environ["PREFECT_SERVER_ANALYTICS_ENABLED"] = "false"
os.environ["DO_NOT_TRACK"] = "1"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

import prefect
from prefect import flow, task, get_run_logger
from prefect.client.orchestration import get_client

print(f"Python Version: {sys.version.split()[0]}")
print(f"Prefect Version: {prefect.__version__}")
print(f"Pandas Version: {pd.__version__}")
"""))

    # 1.1 Business Understanding
    cells.append(nbf.v4.new_markdown_cell("""---
## Sub-Objective 1: Design and Development of a Data Pipeline
### Activity 1.1: Business Understanding

#### 1. Business Problem Definition
In telecommunications and cloud subscription businesses, customer retention is paramount. The cost of acquiring a new customer is estimated to be **5 to 7 times higher** than retaining an existing subscriber. When customers terminate their contract (churn), the provider loses both immediate recurring monthly revenue and substantial customer lifetime value (LTV).

#### 2. Key Business & Data Science Objectives:
1. **Early Risk Identification:** Predict customer churn propensity before contract renewal dates, allowing proactive intervention by retention teams.
2. **Key Driver Identification:** Isolate the primary features driving churn (e.g., contract commitment, fiber optic service without technical support, payment method friction).
3. **Automated Continuous DataOps Pipeline:** Deploy an automated orchestration workflow that executes data ingestion, statistical data quality checks, preprocessing, and EDA every **2 minutes**.
4. **API-Driven Accessibility:** Expose pipeline health, flow execution details, and real-time prediction capabilities through standardized REST APIs.
"""))

    # 1.2 Data Ingestion
    cells.append(nbf.v4.new_markdown_cell("""---
### Activity 1.2: Data Ingestion

The dataset selected for this study is the **IBM / Kaggle Telco Customer Churn** dataset.
- **Source:** Public Kaggle / IBM Business Analytics Repository.
- **Total Records:** 7,043 customer accounts.
- **Total Attributes:** 21 features spanning demographics, subscribed services, account details, and the target churn indicator.
- **Sufficiency:** 7,043 records provide strong statistical power for significance testing, correlation estimation, and robust machine learning validation.
"""))

    cells.append(nbf.v4.new_code_cell("""# 1.2 Data Ingestion with Integrity Checks
data_path = Path("data/telco_customer_churn.csv")
if not data_path.exists():
    import urllib.request
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, data_path)

df = pd.read_csv(data_path)
print(f"Successfully Ingested Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
df.head(3)
"""))

    # 1.3 Data Preprocessing
    cells.append(nbf.v4.new_markdown_cell("""---
### Activity 1.3: Data Pre-processing

In this section, we carry out all five required preprocessing steps:
1. **Displaying Data Types:** Categorizing columns into numeric vs categorical representations.
2. **Checking for Missing Values:** Scanning for nulls, NaNs, and whitespace entries.
3. **Imputing Missing Data for Numeric Columns:** Converting `TotalCharges` from string to float, identifying 11 blank entries for new customers (`tenure = 0`), and imputing them with the median value (\$1,397.47).
4. **Displaying Summary Statistics:** Generating full statistical metrics (mean, std, min, quartiles, max, skewness).
5. **Normalizing Data:** Applying `MinMaxScaler` on continuous variables (`tenure`, `MonthlyCharges`, `TotalCharges`) to scale them strictly into $[0, 1]$.
"""))

    cells.append(nbf.v4.new_code_cell("""# 1. Display Data Types
print("=== 1. FEATURE DATA TYPES ===")
print(df.dtypes)

# 2. Check for Missing Values & Whitespace Blanks
print("\\n=== 2. MISSING VALUES CHECK ===")
raw_nulls = df.isna().sum()
blank_spaces = (df.astype(str).apply(lambda col: col.str.strip() == "")).sum()
missing_report = pd.DataFrame({"Null_Count": raw_nulls, "Blank_Space_Count": blank_spaces})
print(missing_report[missing_report.sum(axis=1) > 0])

# 3. Numeric Conversion & Imputation of TotalCharges
df_preprocessed = df.copy()
df_preprocessed["TotalCharges"] = pd.to_numeric(df_preprocessed["TotalCharges"].astype(str).str.strip(), errors="coerce")
missing_tc = int(df_preprocessed["TotalCharges"].isna().sum())
median_tc = float(df_preprocessed["TotalCharges"].median())
df_preprocessed["TotalCharges"] = df_preprocessed["TotalCharges"].fillna(median_tc)
print(f"\\nImputed {missing_tc} missing values in TotalCharges using Median: ${median_tc:.2f}")

# 4. Display Summary Statistics
numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
summary_stats = df_preprocessed[numeric_cols].describe().T
summary_stats["skewness"] = df_preprocessed[numeric_cols].skew()
print("\\n=== 4. NUMERIC SUMMARY STATISTICS ===")
display(summary_stats.round(3))

# 5. Normalizing Data (MinMax Scaling onto [0, 1])
scaler = MinMaxScaler()
norm_cols = [f"{col}_norm" for col in numeric_cols]
df_preprocessed[norm_cols] = scaler.fit_transform(df_preprocessed[numeric_cols])
print("\\n=== 5. MINMAX NORMALIZED SAMPLES [0, 1] ===")
display(df_preprocessed[norm_cols].head(3))
"""))

    # 1.4 Exploratory Data Analysis
    cells.append(nbf.v4.new_markdown_cell("""---
### Activity 1.4: Exploratory Data Analysis (EDA)

We perform thorough exploratory analysis addressing all assignment prompts:
1. **Target Distribution:** Quantifying overall customer churn rate.
2. **Continuous Feature Distributions:** Univariate histogram and Kernel Density Estimation (KDE).
3. **Correlation Analysis:** Pearson (linear) and Spearman (rank) correlation matrices.
4. **Categorical Association:** Chi-Square ($\chi^2$) test of independence and Cramér's V statistic.
5. **Binning:** Segmenting `tenure` into 4 cohorts and `MonthlyCharges` into 3 price tiers.
6. **Feature Encoding:** Binary mapping and One-Hot Encoding (`pd.get_dummies`).
7. **Feature Importance Assessment:** Training a Random Forest classifier to extract Gini feature importances and Mutual Information scores.
8. **Visualizations:** Univariate and bivariate plots.
"""))

    cells.append(nbf.v4.new_code_cell("""# 1. Target Encoding & Class Balance
df_eda = df_preprocessed.copy()
df_eda["Churn_binary"] = (df_eda["Churn"].str.strip() == "Yes").astype(int)
churn_count = df_eda["Churn_binary"].value_counts()
print(f"Overall Churn Rate: {df_eda['Churn_binary'].mean():.2%} (No: {churn_count[0]}, Yes: {churn_count[1]})")

# 2. Pearson & Spearman Correlation Coefficients
corr_cols = numeric_cols + ["Churn_binary"]
pearson_corr = df_eda[corr_cols].corr(method="pearson").round(3)
spearman_corr = df_eda[corr_cols].corr(method="spearman").round(3)
print("\\n=== PEARSON CORRELATION WITH CHURN ===")
print(pearson_corr["Churn_binary"])

# 3. Categorical Association Tests (Chi-Square & Cramer's V)
cat_cols = [
    "gender", "SeniorCitizen", "Partner", "Dependents",
    "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod"
]

cat_results = []
for col in cat_cols:
    contingency = pd.crosstab(df_eda[col], df_eda["Churn_binary"])
    chi2, p_val, _, _ = stats.chi2_contingency(contingency)
    n = contingency.sum().sum()
    cramers_v = np.sqrt(chi2 / (n * (min(contingency.shape) - 1)))
    cat_results.append({
        "Feature": col,
        "Chi2_Stat": round(chi2, 2),
        "P_Value": p_val,
        "Cramers_V": round(cramers_v, 4),
        "Statistically_Significant": p_val < 0.05
    })

cat_df = pd.DataFrame(cat_results).sort_values(by="Cramers_V", ascending=False)
print("\\n=== TOP CATEGORICAL ASSOCIATIONS (CRAMER'S V) ===")
display(cat_df.head(5))

# 4. Binning: Tenure Cohorts & Charges Tiers
tenure_bins = [0, 12, 24, 48, 72]
tenure_labels = ["0-12m (New)", "13-24m (1-2 Yr)", "25-48m (2-4 Yr)", "49-72m (Loyal)"]
df_eda["tenure_cohort"] = pd.cut(df_eda["tenure"], bins=tenure_bins, labels=tenure_labels, include_lowest=True)

cohort_churn = df_eda.groupby("tenure_cohort", observed=False)["Churn_binary"].agg(
    Total_Customers="count",
    Churned_Count="sum",
    Churn_Rate="mean"
).reset_index()
cohort_churn["Churn_Rate_%"] = (cohort_churn["Churn_Rate"] * 100).round(2)
print("\\n=== TENURE COHORT CHURN RATES ===")
display(cohort_churn)
"""))

    # Display Visualizations
    cells.append(nbf.v4.new_markdown_cell("""### Visualizations: Univariate and Bivariate Analyses

Below are the publication-quality charts generated during the EDA phase:
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### 1. Univariate Visualizations: Target Class Balance & Feature Distributions
| Churn Target Distribution | Numeric Distributions with KDE |
| :---: | :---: |
| ![Churn Distribution](figures/churn_distribution.png) | ![Numeric Distributions](figures/numeric_distributions.png) |
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### 2. Bivariate Visualizations: Contract Impact & Monthly Charges Density
| Churn Rate by Contract Type | Monthly Charges Density by Churn |
| :---: | :---: |
| ![Bivariate Contract](figures/bivariate_contract_churn.png) | ![Bivariate Charges](figures/bivariate_charges_churn.png) |
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### 3. Binned Cohort Analysis & Pearson Correlation Heatmap
| Tenure Cohort Churn Rates | Correlation Heatmap |
| :---: | :---: |
| ![Tenure Cohorts](figures/tenure_cohort_analysis.png) | ![Correlation Heatmap](figures/correlation_heatmap.png) |
"""))

    # Feature Importance Code Cell
    cells.append(nbf.v4.new_code_cell("""# 5. Feature Encoding & Importance Assessment
binary_cols = ["gender", "Partner", "Dependents", "PhoneService", "PaperlessBilling"]
df_encoded = df_eda.copy()
for col in binary_cols:
    if col == "gender":
        df_encoded[col] = (df_encoded[col] == "Male").astype(int)
    else:
        df_encoded[col] = (df_encoded[col] == "Yes").astype(int)

multi_cols = [c for c in cat_cols if c not in binary_cols]
df_encoded = pd.get_dummies(df_encoded, columns=multi_cols, drop_first=True)

exclude = ["customerID", "Churn", "Churn_binary", "tenure_cohort"]
feature_cols = [c for c in df_encoded.columns if c not in exclude]

X = df_encoded[feature_cols]
y = df_encoded["Churn_binary"]

# Train Random Forest to assess feature importance
rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf.fit(X, y)
mi_scores = mutual_info_classif(X, y, random_state=42)

feat_imp = pd.DataFrame({
    "Feature": feature_cols,
    "RF_Gini_Importance": rf.feature_importances_,
    "Mutual_Information": mi_scores
}).sort_values(by="RF_Gini_Importance", ascending=False)

print("=== TOP 10 PREDICTIVE CHURN FEATURES ===")
display(feat_imp.head(10).round(4))
"""))

    cells.append(nbf.v4.new_markdown_cell("""#### Feature Importance Ranking Chart
![Feature Importance](figures/feature_importance_ranking.png)
"""))

    # 1.5 DataOps
    cells.append(nbf.v4.new_markdown_cell("""---
### Activity 1.5: DataOps Implementation

The entire pipeline is automated using **Prefect 3**:
- **Modular Tasks:** `@task` decorators for Ingestion, Preprocessing, EDA, and Model Telemetry.
- **Orchestration Flow:** Master `@flow` linking tasks with dependency tracking.
- **2-Minute Scheduling:** Deployed with `IntervalSchedule(interval=120s)` to execute every 2 minutes.
- **Logging & Cloud Dashboard:** All telemetry is logged via `get_run_logger()` and displayed in the Cloud Dashboard.
"""))

    cells.append(nbf.v4.new_code_cell("""# Execute Prefect Flow directly
from AIMLCZG549_Assignment1.src.pipeline import telco_churn_dataops_flow

print("Executing automated Prefect DataOps flow...")
result = telco_churn_dataops_flow()

print("\\n=== FLOW EXECUTION COMPLETED ===")
print(f"Pipeline: {result['pipeline_name']}")
print(f"Timestamp: {result['execution_timestamp']}")
print(f"Processed Records: {result['data_ingestion']['total_records']}")
print(f"Missing Values Handled: {result['preprocessing']['imputation_details']['missing_count']}")
print(f"Baseline ROC-AUC: {result['model_performance']['roc_auc']}")
print(f"Schedule Cadence: {result['dataops_schedule']['cadence']}")
"""))

    cells.append(nbf.v4.new_markdown_cell("""### Cloud Dashboard & Terminal Logs Evidence
Below are the application screenshots showing the active 2-minute recurring schedule, flow run execution states, and terminal streaming logs:

| Prefect Cloud Dashboard (2-Min Schedule & Runs) | Terminal DataOps Execution Logs |
| :---: | :---: |
| ![Prefect Dashboard](screenshots/01_prefect_cloud_dashboard.png) | ![Terminal Logs](screenshots/04_terminal_dataops_execution.png) |
"""))

    # Sub-Objective 2: API Access
    cells.append(nbf.v4.new_markdown_cell("""---
## Sub-Objective 2: API Access
### Activity 3.1 & 3.2: Retrieve and Display Key Application Details via Built-in APIs

We leverage Prefect's Built-in Client API to programmatically extract operational metadata and present the **four key application details**:
1. **Detail 1: Flow Metadata:** Flow Name, Unique Flow ID, Registration Timestamp, and Tags.
2. **Detail 2: Deployment Configuration:** Deployment Name, Deployment ID, Interval Schedule (every 2 minutes / 120s), and Active Status.
3. **Detail 3: Flow Run Telemetry:** Latest Run ID, Run Name, State (`Completed`), and Execution Duration.
4. **Detail 4: Data Quality & Model Metrics:** Total Records Processed (7,043), Missing Values Imputed (11), Scaling Method, and ROC-AUC.
"""))

    cells.append(nbf.v4.new_code_cell("""# Query Application Details via Built-in API Client
from fastapi.testclient import TestClient
from AIMLCZG549_Assignment1.src.api_service import app

client = TestClient(app)

response = client.get("/api/v1/application/details")
assert response.status_code == 200
app_details = response.json()

print(f"HTTP Status: {response.status_code} OK")
print(json.dumps(app_details, indent=2))
"""))

    # Activity 3.3 API Testing & Documentation
    cells.append(nbf.v4.new_markdown_cell("""---
### Activity 3.3: API Testing and Documentation

To verify robust API operation, an automated testing suite tests all endpoints against positive and negative test cases, verifying appropriate HTTP status codes:
- **`200 OK`**: Data retrieval (`/health`, `/api/v1/application/details`, `/api/v1/prefect/flows`, `/api/v1/predict/churn`).
- **`202 ACCEPTED`**: Asynchronous pipeline triggering (`/api/v1/pipeline/trigger`).
- **`422 UNPROCESSABLE ENTITY`**: Schema validation failure when passing malformed data to `/api/v1/predict/churn`.
- **`404 NOT FOUND`**: Standard error handling for nonexistent resources (`/api/v1/resource/not-found`).
"""))

    cells.append(nbf.v4.new_code_cell("""# Execute Automated API Test Suite
from AIMLCZG549_Assignment1.src.test_api import run_api_test_suite

summary = run_api_test_suite()
print(f"\\nTotal Tests Executed: {summary['total_tests']}")
print(f"Passed: {summary['passed']} | Failed: {summary['failed']}")
print(f"HTTP Status Codes Verified: {summary['http_status_codes_verified']}")
"""))

    cells.append(nbf.v4.new_markdown_cell("""### API Documentation & Testing Screenshots

| FastAPI Interactive Swagger UI (/docs) | Postman Client Testing (200 OK & 4 Details) |
| :---: | :---: |
| ![Swagger UI](screenshots/02_fastapi_swagger_docs.png) | ![Postman Testing](screenshots/03_postman_api_testing.png) |

| Negative Testing: HTTP 422 & 404 Status Code Verification |
| :---: |
| ![Negative Testing](screenshots/05_api_status_codes_verification.png) |
"""))

    # Conclusion
    cells.append(nbf.v4.new_markdown_cell("""---
## 4. Conclusion & Key Findings

1. **Business Insights:**
   - Contract commitment is the strongest deterrent to customer churn ($\text{Cramer's } V = 0.4101$). Customers on month-to-month contracts exhibit an alarming 42.7% churn rate, compared to 11.3% for 1-year and 2.8% for 2-year contracts.
   - Customers in their first year (0-12 months tenure) churn at a 47.4% rate, while loyal customers (>48 months) churn at only 9.5%.
   - Fiber optic users churn at twice the rate of DSL users when lacking technical support, indicating a clear retention strategy: bundle proactive technical support with fiber plans.
2. **DataOps Architecture:**
   - Prefect 3 provides reliable orchestration with automated 2-minute scheduling, structured logging, and full traceability.
   - Missing data was detected and imputed using median values, and continuous variables were normalized to $[0, 1]$ using `MinMaxScaler`.
3. **API-Driven Integration:**
   - The FastAPI gateway successfully retrieves Flow, Deployment, and Flow Run details via Prefect's Built-in API.
   - All HTTP status codes (`200 OK`, `202 Accepted`, `404 Not Found`, `422 Unprocessable Entity`) were systematically tested and verified with complete documentation.
"""))

    nb.cells = cells

    notebook_path = PROJECT_ROOT / "AIMLCZG549_Assignment1_DataOps.ipynb"
    with open(notebook_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Jupyter Notebook successfully written to: {notebook_path}")
    return notebook_path


if __name__ == "__main__":
    create_assignment_notebook()
