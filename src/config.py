"""
Configuration module for AIMLCZG549 Assignment 1:
Telco Customer Churn DataOps Pipeline & Cloud-Native API Service.
"""
from pathlib import Path
import os

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "telco_customer_churn.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_telco_churn.csv"
PIPELINE_METRICS_PATH = DATA_DIR / "pipeline_metrics.json"

# Figures and Outputs
FIGURES_DIR = PROJECT_ROOT / "figures"
TEST_RESULTS_DIR = PROJECT_ROOT / "test_results"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

# Ensure output directories exist
for directory in [DATA_DIR, FIGURES_DIR, TEST_RESULTS_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Prefect Configuration
PREFECT_HOME_DIR = PROJECT_ROOT / ".prefect"
PREFECT_HOME_DIR.mkdir(parents=True, exist_ok=True)
os.environ["PREFECT_HOME"] = str(PREFECT_HOME_DIR)
os.environ["PREFECT_SERVER_ANALYTICS_ENABLED"] = "false"
os.environ["DO_NOT_TRACK"] = "1"

FLOW_NAME = "telco-customer-churn-dataops-pipeline"
DEPLOYMENT_NAME = "churn-dataops-2min-deployment"
SCHEDULE_INTERVAL_SECONDS = 120  # Runs every 2 minutes as required by Sub-Objective 1.5

# Server & API Ports
API_HOST = "127.0.0.1"
API_PORT = 8000
PREFECT_API_URL = "http://127.0.0.1:4200/api"

# Dataset Column Definitions
TARGET_COLUMN = "Churn"
ID_COLUMN = "customerID"

NUMERIC_COLUMNS = ["tenure", "MonthlyCharges", "TotalCharges"]

CATEGORICAL_COLUMNS = [
    "gender", "SeniorCitizen", "Partner", "Dependents",
    "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod"
]

BINARY_COLUMNS = [
    "gender", "Partner", "Dependents", "PhoneService", "PaperlessBilling"
]

# Binning Definitions
TENURE_BINS = [0, 12, 24, 48, 72]
TENURE_LABELS = ["0-12m (New)", "13-24m (1-2 Yr)", "25-48m (2-4 Yr)", "49-72m (Loyal)"]

CHARGES_BINS = [0, 35, 70, 150]
CHARGES_LABELS = ["Low (<$35)", "Medium ($35-$70)", "High (>$70)"]
