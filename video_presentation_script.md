# AIMLCZG549: API-driven Cloud Native Solutions
## Assignment I — Video Demonstration Walkthrough Script
**Target Duration:** 5 to 7 Minutes  
**Component:** Continuous Evaluation (EC-1) | **Weightage:** 15 Marks | **Group ID:** 80  
**Project:** Cloud-Based Data Science Pipeline & API-Driven Architecture (Customer Churn Prevention)

---

### **Student Presenter:**
- **SREE TEJA R (2025AE05629)** — 100% Contribution (End-to-End Pipeline, DataOps & Cloud-Native API Architecture)

---

### **Segment 1: Project Introduction & Architecture (0:00 – 1:00)**
**Presenter:** *SREE TEJA R*  
**On-Screen Display:** Title slide, followed by `Figure 1: End-to-End Cloud-Native Architecture Diagram`.

> *"Hello everyone and respected professors. Welcome to the demonstration of Assignment I for AIMLCZG549: API-driven Cloud Native Solutions, submitted under Group ID 80.*
> 
> *My name is Sree Teja R (Student ID: 2025AE05629). I have developed an end-to-end, production-grade cloud-native Data Science and DataOps application addressing Customer Churn Prevention in Telecommunication and Subscription Platforms.*
> 
> *In subscription industries, acquiring a new subscriber costs five to seven times more than retaining an existing customer. This project achieves two core sub-objectives:*
> *First, Sub-Objective 1: Building an automated DataOps pipeline orchestrating data ingestion, statistical data quality checks, missing value imputation, MinMax normalization, and exploratory analysis scheduled to run every two minutes using Prefect 3.*
> *Second, Sub-Objective 2: Providing cloud-native API access to internal flow definitions, deployments, execution telemetry, and real-time inference via a FastAPI gateway.*
> 
> *Let us now dive into the Data Ingestion and Pre-processing implementation."*

---

### **Segment 2: Data Ingestion & Pre-processing (1:00 – 2:15)**
**Presenter:** *SREE TEJA R*  
**On-Screen Display:** Jupyter Notebook cells for Section 1.2 and 1.3, code editor showing `src/pipeline.py`.

> *"Moving to Sub-Objective 1, Activities 1.2 and 1.3:*
> 
> *For data ingestion, I sourced the IBM / Kaggle Telco Customer Churn dataset, comprising 7,043 customer accounts across 21 attributes. This volume provides high statistical power for modeling and hypothesis testing.*
> 
> *During data profiling and preprocessing, five key activities were completed programmatically:*
> *1. Feature Data Types: Mapped 17 categorical features and 3 continuous variables—tenure, Monthly Charges, and Total Charges.*
> *2. Missing Value Detection: Identified 11 blank whitespace entries in TotalCharges corresponding to brand-new accounts with tenure equal to zero.*
> *3. Missing Data Imputation: Rather than discarding records, TotalCharges was coerced to numeric and imputed using the median value of $1,397.47, maintaining statistical integrity.*
> *4. Summary Statistics: Computed parametric and non-parametric metrics including count, mean, standard deviation, quartiles, and skewness.*
> *5. Data Normalization: Applied MinMaxScaler to scale tenure, Monthly Charges, and Total Charges strictly into the interval [0, 1], guaranteeing numerical stability for machine learning.*
> 
> *Next, let us look at the Exploratory Data Analysis."*

---

### **Segment 3: Exploratory Data Analysis & Visualizations (2:15 – 3:30)**
**Presenter:** *SREE TEJA R*  
**On-Screen Display:** Notebook plots, `figures/churn_distribution.png`, `figures/bivariate_contract_churn.png`, `figures/tenure_cohort_analysis.png`, `figures/correlation_heatmap.png`.

> *"In Activity 1.4, I conducted thorough Exploratory Data Analysis across multiple dimensions:*
> 
> *First, examining target class balance: our baseline churn rate is 26.54%, with 1,869 churned customers out of 7,043.*
> 
> *Second, bivariate analysis revealed that Contract Type is the single strongest determinant of churn. Month-to-month subscribers experience an alarming 42.7% churn rate, compared to just 11.3% for one-year and 2.8% for two-year contracts.*
> 
> *Third, Chi-Square tests of independence and Cramér’s V statistics confirmed strong categorical associations for Contract (Cramér's V = 0.4101, p < 10⁻²⁵⁰), Online Security (V = 0.3474), and Tech Support (V = 0.3429).*
> 
> *Fourth, I performed binning on customer tenure into four cohorts. Customers in their first year (0 to 12 months) churn at 47.4%, whereas loyal customers past 48 months churn at only 9.5%.*
> 
> *Finally, Pearson and Spearman correlation matrices showed significant negative correlations between customer tenure and churn propensity (-0.352).*
> 
> *Let us now look at feature importance and our DataOps automation."*

---

### **Segment 4: Feature Importance & DataOps 2-Minute Scheduling (3:30 – 4:45)**
**Presenter:** *SREE TEJA R*  
**On-Screen Display:** `figures/feature_importance_ranking.png`, live terminal showing `prefect` execution, Prefect Cloud Dashboard (`screenshots/01_prefect_cloud_dashboard.png`).

> *"Continuing in Activity 1.4, I encoded categorical features using binary mapping and One-Hot Encoding, and trained a Random Forest Classifier.*
> 
> *Evaluating Gini importance and Mutual Information confirmed our top predictive churn drivers: tenure, Total Charges, Monthly Charges, Month-to-month contract, and Fiber Optic internet service.*
> 
> *Moving to Activity 1.5 DataOps:*
> *The entire workflow is orchestrated using Prefect 3. Each stage—ingestion, preprocessing, EDA, and model evaluation—is a modular task with automated retry policies.*
> *I deployed the pipeline with an Interval Schedule of 120 seconds—exactly two minutes—as mandated by the assignment.*
> 
> *As visible on the screen in our Prefect Cloud Dashboard, the pipeline triggers every two minutes automatically. All activity details, record counts, imputation statistics, and baseline ROC-AUC scores (0.8245) are streamed live into the dashboard logs.*
> 
> *Now, let us examine our API access and verification."*

---

### **Segment 5: Sub-Objective 2: API Access, Demonstration & Verification (4:45 – 6:15)**
**Presenter:** *SREE TEJA R*  
**On-Screen Display:** Swagger UI (`http://127.0.0.1:8000/docs`), Postman Client, `screenshots/03_postman_api_testing.png`, `screenshots/05_api_status_codes_verification.png`.

> *"Under Sub-Objective 2: API Access, I implemented a robust dual API layer:*
> 
> *First, in Activity 3.1, I utilized Prefect's Built-in Client APIs to programmatically retrieve flow definitions, deployments, and flow run execution states.*
> 
> *Second, in Activity 3.2, I expose the four mandatory application details through our dedicated endpoint: GET /api/v1/application/details.*
> *As demonstrated in Postman, this endpoint returns:*
> *1. Detail 1 (Flow Metadata): Flow Name 'telco-customer-churn-dataops-pipeline' and unique Flow ID.*
> *2. Detail 2 (Deployment Config): Deployment Name, status READY, and the active two-minute schedule.*
> *3. Detail 3 (Flow Run Telemetry): Latest Run 'pretty-jackal', status Completed, and 1.92s duration.*
> *4. Detail 4 (Pipeline Telemetry): 7,043 processed rows, 11 median-imputed values, and model ROC-AUC.*
> 
> *Third, in Activity 3.3, I developed an automated test suite validating 12 test cases with strict HTTP status code verification:*
> *- 200 OK for successful data retrieval and real-time ML inference.*
> *- 202 ACCEPTED when triggering on-demand pipeline runs asynchronously.*
> *- 422 UNPROCESSABLE ENTITY when passing invalid customer schemas, demonstrating rigorous Pydantic validation.*
> *- And 404 NOT FOUND for nonexistent resource routes.*
> 
> *To conclude, this project bridges modern DataOps automation with cloud-native API microservices, fully satisfying every requirement of Assignment I. Thank you for your time!"*

---
### **Video Recording Checklist:**
- [x] Clear screen recording with audio voiceover from SREE TEJA R (2025AE05629).
- [x] Demonstrates Prefect Cloud Dashboard showing the active 2-minute recurring schedule.
- [x] Demonstrates live Postman and Swagger UI `/docs` requests showing HTTP status codes 200, 202, 404, 422.
- [x] Upload video file to Google Drive and verify link permissions are set to "Anyone with the link can view".
