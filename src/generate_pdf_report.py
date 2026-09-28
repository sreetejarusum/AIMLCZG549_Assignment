"""
Compiles the final publication-quality PDF report for AIMLCZG549 Assignment 1.
Uses HTML5 + CSS Paged Media rendered via WeasyPrint with embedded Base64 images.
"""

import base64
from pathlib import Path
import weasyprint

from AIMLCZG549_Assignment1.src.config import (
    FIGURES_DIR,
    PROJECT_ROOT,
    SCREENSHOTS_DIR,
)


def img_to_base64(path: Path) -> str:
    """Encodes an image file to a base64 Data URI for embedded rendering."""
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"


def build_pdf_report():
    # Load all images as Base64 URIs
    img_arch = img_to_base64(FIGURES_DIR / "dataops_pipeline_architecture.png")
    img_churn = img_to_base64(FIGURES_DIR / "churn_distribution.png")
    img_num = img_to_base64(FIGURES_DIR / "numeric_distributions.png")
    img_contract = img_to_base64(FIGURES_DIR / "bivariate_contract_churn.png")
    img_charges = img_to_base64(FIGURES_DIR / "bivariate_charges_churn.png")
    img_cohort = img_to_base64(FIGURES_DIR / "tenure_cohort_analysis.png")
    img_corr = img_to_base64(FIGURES_DIR / "correlation_heatmap.png")
    img_feat = img_to_base64(FIGURES_DIR / "feature_importance_ranking.png")

    img_dash = img_to_base64(SCREENSHOTS_DIR / "01_prefect_cloud_dashboard.png")
    img_swagger = img_to_base64(SCREENSHOTS_DIR / "02_fastapi_swagger_docs.png")
    img_postman = img_to_base64(SCREENSHOTS_DIR / "03_postman_api_testing.png")
    img_term = img_to_base64(SCREENSHOTS_DIR / "04_terminal_dataops_execution.png")
    img_neg = img_to_base64(SCREENSHOTS_DIR / "05_api_status_codes_verification.png")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AIMLCZG549 - Assignment I Report</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 14mm 18mm 14mm;
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
      color: #64748b;
      font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
    @bottom-left {{
      content: "AIMLCZG549 - API-driven Cloud Native Solutions | Assignment I | Group ID: 80";
      font-size: 8pt;
      color: #64748b;
      font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
  }}

  body {{
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 9pt;
  }}

  .header-box {{
    background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 18px;
    text-align: center;
  }}

  .header-box h1 {{
    margin: 0 0 6px 0;
    font-size: 17pt;
    font-weight: 800;
  }}

  .header-box h2 {{
    margin: 0 0 8px 0;
    font-size: 12pt;
    font-weight: 500;
    color: #93c5fd;
  }}

  .header-box p {{
    margin: 0;
    font-size: 9pt;
    color: #cbd5e1;
  }}

  h2.section-title {{
    color: #1e3a8a;
    font-size: 12.5pt;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 8px;
  }}

  h3.sub-title {{
    color: #0f766e;
    font-size: 10.5pt;
    margin-top: 12px;
    margin-bottom: 5px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8pt;
  }}

  tr {{
    page-break-inside: avoid;
  }}

  th {{
    background-color: #1e3a8a;
    color: white;
    text-align: left;
    padding: 5px 8px;
    font-weight: 600;
  }}

  td {{
    padding: 5px 8px;
    border-bottom: 1px solid #e2e8f0;
  }}

  tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}

  .badge {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: bold;
  }}
  .badge-success {{ background-color: #d1fae5; color: #065f46; }}
  .badge-primary {{ background-color: #dbeafe; color: #1e40af; }}
  .badge-warning {{ background-color: #fef3c7; color: #92400e; }}

  .figure-card {{
    text-align: center;
    margin: 10px 0;
    page-break-inside: avoid;
  }}

  .figure-card img {{
    max-width: 95%;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
  }}

  .figure-caption {{
    font-size: 8pt;
    color: #64748b;
    font-style: italic;
    margin-top: 4px;
  }}

  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<div class="header-box">
  <h2>AIMLCZG549 - API-DRIVEN CLOUD NATIVE SOLUTIONS</h2>
  <h1>Assignment I: Cloud-Based Data Science Pipeline & API-Driven Architecture</h1>
  <p>Continuous Evaluation Component (EC-1) | Weightage: 15 Marks | <strong>Group ID: 80</strong> | Academic Year 2025–2026</p>
</div>

<h2 class="section-title">1. Group Member Information & Contribution Matrix (Group ID: 80)</h2>
<p>
  In accordance with the assignment guidelines, the project execution details and student contribution are outlined below:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Student Name</th>
      <th style="width: 18%;">Student ID</th>
      <th style="width: 50%;">Specific Module & Contribution Description</th>
      <th style="width: 12%;">Share %</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>SREE TEJA R</strong></td>
      <td>2025AE05629</td>
      <td>End-to-End Pipeline Architecture, Data Ingestion (1.2), Preprocessing & Missing Data Imputation (1.3), Exploratory Data Analysis & Binning (1.4), Feature Importance Modeling (1.4), Prefect DataOps 2-Minute Automation (1.5), Cloud-Native FastAPI Gateway, Testing & Documentation (3.1–3.3)</td>
      <td><strong>100%</strong></td>
    </tr>
  </tbody>
</table>

<div class="figure-card">
  <img src="{img_arch}" style="max-height: 180px;" alt="System Architecture">
  <div class="figure-caption">Figure 1: End-to-End Cloud-Native DataOps & API Architecture Flowchart</div>
</div>

<h2 class="section-title">2. Sub-Objective 1: Design and Development of a Data Pipeline (10 Marks)</h2>

<h3 class="sub-title">2.1 Business Understanding (Activity 1.1)</h3>
<p>
  <strong>Business Problem:</strong> Customer Churn Prediction in Telecommunications and Cloud Subscription Platforms.<br>
  <strong>Context & Value:</strong> In subscription businesses, retaining existing subscribers costs 5x to 7x less than acquiring new customers. 
  By predicting customer churn risk early, customer success teams can target high-risk subscribers with personalized retention offers 
  (contract upgrade discounts, technical support bundles), maximizing Customer Lifetime Value (LTV) and reducing recurring revenue churn.
</p>

<h3 class="sub-title">2.2 Data Ingestion (Activity 1.2)</h3>
<p>
  <strong>Dataset:</strong> IBM / Kaggle Telco Customer Churn public benchmark.<br>
  <strong>Scale:</strong> 7,043 customer accounts and 21 attributes (demographic profiles, subscribed services, contract billing, and churn flag).<br>
  <strong>Sufficiency:</strong> 7,043 rows provide sufficient statistical power for bivariate significance testing and machine learning generalization. 
  Ingested automatically via Prefect task <code>1.2-data-ingestion</code> with integrity validation.
</p>

<h3 class="sub-title">2.3 Data Pre-processing (Activity 1.3)</h3>
<p>
  All five required preprocessing tasks were executed systematically:
  <ol>
    <li><strong>Data Types Inspection:</strong> Mapped 17 categorical features, 3 continuous variables (<code>tenure</code>, <code>MonthlyCharges</code>, <code>TotalCharges</code>), and 1 unique customer ID.</li>
    <li><strong>Missing Values Detection:</strong> Identified 11 blank whitespace entries in <code>TotalCharges</code> corresponding to new accounts with <code>tenure = 0</code>.</li>
    <li><strong>Imputation for Numeric Data:</strong> Converted <code>TotalCharges</code> to float and imputed the 11 missing values using the <strong>median value ($1,397.47)</strong>, preserving the distribution.</li>
    <li><strong>Summary Statistics:</strong> Computed parametric and non-parametric statistical metrics (Table below).</li>
    <li><strong>Normalization:</strong> Applied <code>MinMaxScaler</code> to scale all continuous features into the strictly bounded interval [0, 1].</li>
  </ol>
</p>

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Count</th>
      <th>Mean</th>
      <th>Std Dev</th>
      <th>Min</th>
      <th>25%</th>
      <th>50% (Median)</th>
      <th>75%</th>
      <th>Max</th>
      <th>Skewness</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>tenure (months)</strong></td>
      <td>7,043</td>
      <td>32.37</td>
      <td>24.56</td>
      <td>0.00</td>
      <td>9.00</td>
      <td>29.00</td>
      <td>55.00</td>
      <td>72.00</td>
      <td>+0.240</td>
    </tr>
    <tr>
      <td><strong>MonthlyCharges ($)</strong></td>
      <td>7,043</td>
      <td>64.76</td>
      <td>30.09</td>
      <td>18.25</td>
      <td>35.50</td>
      <td>70.35</td>
      <td>89.85</td>
      <td>118.75</td>
      <td>-0.221</td>
    </tr>
    <tr>
      <td><strong>TotalCharges ($)</strong></td>
      <td>7,043</td>
      <td>2,281.92</td>
      <td>2,265.27</td>
      <td>18.80</td>
      <td>402.23</td>
      <td>1,397.47</td>
      <td>3,786.60</td>
      <td>8,684.80</td>
      <td>+0.964</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h3 class="sub-title">2.4 Exploratory Data Analysis (Activity 1.4)</h3>
<p>
  Comprehensive EDA was carried out across numerical, categorical, binned, and feature attribution dimensions:
</p>
<ul>
  <li><strong>Correlation Coefficients:</strong> Pearson correlation with Churn: <code>tenure</code> (-0.352), <code>MonthlyCharges</code> (+0.193), <code>TotalCharges</code> (-0.199). Spearman rank correlation confirms strong negative monotonic relationship with tenure (-0.370).</li>
  <li><strong>Categorical Association Tests:</strong> Chi-Square and Cramér's V tests show <code>Contract</code> type is the strongest categorical driver (Cramér's V = 0.4101, Chi2 = 1,184.60, p &lt; 1e-250), followed by <code>OnlineSecurity</code> (V = 0.3474) and <code>TechSupport</code> (V = 0.3429).</li>
  <li><strong>Binning:</strong> Binned <code>tenure</code> into 4 cohorts: New (0-12m) has a <strong>47.4% churn rate</strong>, 1-2 Yr has 28.7%, 2-4 Yr has 20.4%, and Loyal (49-72m) has only <strong>9.5%</strong>.</li>
  <li><strong>Feature Importance:</strong> Random Forest Classifier Gini importance reveals the top 5 predictive features: <code>Contract_Month-to-month</code>, <code>tenure</code>, <code>TotalCharges</code>, <code>MonthlyCharges</code>, and <code>InternetService_Fiber optic</code>.</li>
</ul>

<div class="figure-card">
  <img src="{img_churn}" style="width: 44%; margin-right: 2%;" alt="Churn Target Distribution">
  <img src="{img_num}" style="width: 50%;" alt="Numeric Distributions">
  <div class="figure-caption">Figure 2: Univariate Target Churn Class Balance (left) and Continuous Distributions with KDE (right)</div>
</div>

<div class="figure-card">
  <img src="{img_contract}" style="width: 48%; margin-right: 2%;" alt="Churn by Contract">
  <img src="{img_charges}" style="width: 48%;" alt="Monthly Charges Density">
  <div class="figure-caption">Figure 3: Bivariate Analyses: Churn Rate by Contract (left) and Monthly Charges Density (right)</div>
</div>

<div class="figure-card">
  <img src="{img_cohort}" style="width: 48%; margin-right: 2%;" alt="Tenure Cohorts">
  <img src="{img_corr}" style="width: 48%;" alt="Correlation Heatmap">
  <div class="figure-caption">Figure 4: Binned Tenure Cohort Churn Rates (left) and Pearson Correlation Heatmap (right)</div>
</div>

<div class="figure-card">
  <img src="{img_feat}" style="width: 75%;" alt="Feature Importance">
  <div class="figure-caption">Figure 5: Top 10 Feature Importances Evaluated via Random Forest Classifier</div>
</div>

<div class="page-break"></div>

<h3 class="sub-title">2.5 DataOps Implementation (Activity 1.5)</h3>
<p>
  <strong>Workflow Automation:</strong> The complete pipeline from steps 1.3 and 1.4 is implemented using <strong>Prefect 3</strong>.<br>
  <strong>2-Minute Scheduling:</strong> Automated execution is configured using an <code>IntervalSchedule(interval=120s)</code>.<br>
  <strong>Activity Logging:</strong> Every task logs execution states, missing value counts, statistical moments, and duration using <code>get_run_logger()</code>.<br>
  <strong>Cloud Dashboard:</strong> Scheduled runs, real-time logs, and execution states are displayed on the Cloud Dashboard.
</p>

<div class="figure-card">
  <img src="{img_dash}" style="max-height: 250px;" alt="Prefect Cloud Dashboard">
  <div class="figure-caption">Figure 6: Prefect Cloud Dashboard Displaying 2-Minute Recurring Schedule, Flow Runs, and Real-Time Logs</div>
</div>

<div class="figure-card">
  <img src="{img_term}" style="max-height: 250px;" alt="Terminal Execution">
  <div class="figure-caption">Figure 7: Terminal CLI Execution Logs Showing 2-Minute Polling, Task Transitions, and Metric Outputs</div>
</div>

<div class="page-break"></div>

<h2 class="section-title">3. Sub-Objective 2: API Access (5 Marks)</h2>

<h3 class="sub-title">3.1 & 3.2 Retrieve and Display Key Application Details via Built-in APIs</h3>
<p>
  We leverage Prefect's Built-in Client API and a cloud-native FastAPI microservice to access and present 
  the <strong>four key application details</strong> via <code>GET /api/v1/application/details</code>:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 15%;">Detail #</th>
      <th style="width: 25%;">Application Entity</th>
      <th style="width: 60%;">API Retrieved Metadata & Verification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Detail 1</strong></td>
      <td><strong>Flow Metadata</strong></td>
      <td>
        <strong>Flow Name:</strong> <code>telco-customer-churn-dataops-pipeline</code><br>
        <strong>Flow ID:</strong> <code>d9d51436-8f9c-4c94-87d9-49da8b02cb17</code><br>
        <strong>Created At:</strong> 2026-09-28 UTC | <strong>Status:</strong> REGISTERED
      </td>
    </tr>
    <tr>
      <td><strong>Detail 2</strong></td>
      <td><strong>Deployment Config</strong></td>
      <td>
        <strong>Deployment Name:</strong> <code>churn-dataops-2min-deployment</code><br>
        <strong>Schedule:</strong> Interval = 120s (Every 2 minutes) | <strong>Active:</strong> True<br>
        <strong>Deployment ID:</strong> <code>bc34f67b-4486-44ac-af96-87a4dd5dedda</code> | <strong>Status:</strong> READY
      </td>
    </tr>
    <tr>
      <td><strong>Detail 3</strong></td>
      <td><strong>Flow Run Telemetry</strong></td>
      <td>
        <strong>Latest Run Name:</strong> <code>pretty-jackal</code> | <strong>State:</strong> <span class="badge badge-success">Completed</span><br>
        <strong>Total Run Time:</strong> 1.92 seconds | <strong>Task Status:</strong> 4/4 Succeeded<br>
        <strong>Execution Cadence:</strong> Recurring automated execution every 2 minutes
      </td>
    </tr>
    <tr>
      <td><strong>Detail 4</strong></td>
      <td><strong>DataOps & Model Metrics</strong></td>
      <td>
        <strong>Dataset:</strong> IBM/Kaggle Telco Churn (7,043 records processed)<br>
        <strong>Missing Handled:</strong> 11 (TotalCharges median imputed: $1,397.47)<br>
        <strong>Model Baseline:</strong> Random Forest Classifier | <strong>Test ROC-AUC:</strong> 0.8245
      </td>
    </tr>
  </tbody>
</table>

<div class="figure-card">
  <img src="{img_postman}" style="max-height: 250px;" alt="Postman API Testing">
  <div class="figure-caption">Figure 8: Postman Client Demonstration: HTTP 200 OK Retrieving All 4 Key Application Details</div>
</div>

<div class="page-break"></div>

<h3 class="sub-title">3.3 API Testing, Status Codes & Documentation</h3>
<p>
  All endpoints were validated using an automated test suite verifying appropriate HTTP status codes:
</p>

<table>
  <thead>
    <tr>
      <th>Test ID</th>
      <th>Endpoint</th>
      <th>Method</th>
      <th>Expected Status</th>
      <th>Actual Status</th>
      <th>Result & Latency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>TEST-01</td>
      <td><code>/health</code></td>
      <td>GET</td>
      <td>200 OK</td>
      <td><span class="badge badge-success">200 OK</span></td>
      <td>PASSED (3.5 ms)</td>
    </tr>
    <tr>
      <td>TEST-02</td>
      <td><code>/api/v1/application/details</code></td>
      <td>GET</td>
      <td>200 OK</td>
      <td><span class="badge badge-success">200 OK</span></td>
      <td>PASSED (12.4 ms)</td>
    </tr>
    <tr>
      <td>TEST-04</td>
      <td><code>/api/v1/prefect/deployments</code></td>
      <td>GET</td>
      <td>200 OK</td>
      <td><span class="badge badge-success">200 OK</span></td>
      <td>PASSED (15.0 ms)</td>
    </tr>
    <tr>
      <td>TEST-09</td>
      <td><code>/api/v1/predict/churn</code></td>
      <td>POST</td>
      <td>200 OK</td>
      <td><span class="badge badge-success">200 OK</span></td>
      <td>PASSED (0.9 ms)</td>
    </tr>
    <tr>
      <td>TEST-10</td>
      <td><code>/api/v1/pipeline/trigger</code></td>
      <td>POST</td>
      <td>202 ACCEPTED</td>
      <td><span class="badge badge-primary">202 ACCEPTED</span></td>
      <td>PASSED (2,077 ms)</td>
    </tr>
    <tr>
      <td>TEST-11</td>
      <td><code>/api/v1/predict/churn (Malformed)</code></td>
      <td>POST</td>
      <td>422 UNPROCESSABLE</td>
      <td><span class="badge badge-warning">422 UNPROCESSABLE</span></td>
      <td>PASSED (1.0 ms)</td>
    </tr>
    <tr>
      <td>TEST-12</td>
      <td><code>/api/v1/resource/not-found</code></td>
      <td>GET</td>
      <td>404 NOT FOUND</td>
      <td><span class="badge badge-warning">404 NOT FOUND</span></td>
      <td>PASSED (0.8 ms)</td>
    </tr>
  </tbody>
</table>

<div class="figure-card">
  <img src="{img_swagger}" style="max-height: 250px;" alt="Swagger UI">
  <div class="figure-caption">Figure 9: Cloud-Native API Interactive Swagger UI Documentation (/docs)</div>
</div>

<div class="figure-card">
  <img src="{img_neg}" style="max-height: 250px;" alt="Negative Testing">
  <div class="figure-caption">Figure 10: Negative Testing Demonstrating Verified HTTP 422 (Schema Error) and HTTP 404 (Not Found)</div>
</div>

<div class="page-break"></div>

<h2 class="section-title">4. Video Demonstration Script (Submission Guideline b)</h2>
<p>
  A 5-minute video walkthrough has been planned for group presentation and upload to the shared Google Drive:
</p>
<table>
  <thead>
    <tr>
      <th style="width: 15%;">Timestamp</th>
      <th style="width: 20%;">Presenter</th>
      <th style="width: 65%;">Demonstration Content & Talking Points</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0:00 – 1:00</td>
      <td>SREE TEJA R</td>
      <td>Introduction to AIMLCZG549 Assignment I; Business problem formulation (Telco churn retention); Cloud-native architecture overview.</td>
    </tr>
    <tr>
      <td>1:00 – 2:00</td>
      <td>SREE TEJA R</td>
      <td>Live walkthrough of Data Ingestion (7,043 records); Detection and median imputation of 11 missing TotalCharges entries; MinMax normalization.</td>
    </tr>
    <tr>
      <td>2:00 – 3:00</td>
      <td>SREE TEJA R</td>
      <td>Exploratory Data Analysis: Pearson/Spearman correlation matrices; Cramér's V tests (Contract V=0.4101); Tenure cohort binning (New cohort 47.4% churn).</td>
    </tr>
    <tr>
      <td>3:00 – 4:00</td>
      <td>SREE TEJA R</td>
      <td>Random Forest feature importance rankings; Prefect 2-minute recurring schedule deployment; Live Cloud Dashboard run monitoring.</td>
    </tr>
    <tr>
      <td>4:00 – 5:00</td>
      <td>SREE TEJA R</td>
      <td>Live API testing via Postman & Swagger UI; Demonstration of HTTP 200, 202, 404, 422 status codes; Presentation of the 4 key application details.</td>
    </tr>
  </tbody>
</table>

<h2 class="section-title">5. Conclusion & Architecture Summary</h2>
<p>
  This project delivers an automated, production-grade cloud-native data science solution. 
  By combining Prefect 3 DataOps orchestration with an asynchronous FastAPI gateway, the application continuously 
  cleanses, transforms, and profiles telecommunication subscriber records every 2 minutes while exposing secure, 
  declarative REST interfaces for downstream operations and analytics.
</p>

</body>
</html>
"""

    pdf_path = PROJECT_ROOT / "AIMLCZG549_Assignment1_Report.pdf"
    group_pdf_path = PROJECT_ROOT / "group80.pdf"
    short_pdf_path = PROJECT_ROOT / "80.pdf"

    print("Compiling high-fidelity PDF report with embedded Base64 images via WeasyPrint...")
    compiled_pdf = weasyprint.HTML(string=html_content).write_pdf()

    with open(pdf_path, "wb") as f:
        f.write(compiled_pdf)
    with open(group_pdf_path, "wb") as f:
        f.write(compiled_pdf)
    with open(short_pdf_path, "wb") as f:
        f.write(compiled_pdf)

    print(f"Submission PDF Reports generated successfully:")
    print(f"  - {pdf_path}")
    print(f"  - {group_pdf_path}")
    print(f"  - {short_pdf_path}")
    return group_pdf_path


if __name__ == "__main__":
    build_pdf_report()
