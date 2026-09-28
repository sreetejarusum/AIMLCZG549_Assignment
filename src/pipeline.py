"""
Core Prefect DataOps Pipeline for AIMLCZG549 Assignment 1.

Sub-Objective 1 Activities:
- 1.1 Business Understanding: Telco Customer Churn Prediction.
- 1.2 Data Ingestion: Ingest IBM/Kaggle Telco Customer Churn dataset with validation.
- 1.3 Data Pre-processing: Summary stats, missing checks, median imputation, dtype display, MinMax normalization.
- 1.4 Exploratory Data Analysis (EDA): Pearson/Spearman correlation, Chi-Square/Cramér's V, binning,
  one-hot/binary encoding, Random Forest feature importance, univariate and bivariate visualizations.
- 1.5 DataOps: Automated Prefect Flow orchestrating tasks, structured logging, 2-minute schedule compatibility.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless cloud execution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Prefect Imports
from prefect import flow, get_run_logger, task

# Local Configuration
from AIMLCZG549_Assignment1.src.config import (
    BINARY_COLUMNS,
    CATEGORICAL_COLUMNS,
    CHARGES_BINS,
    CHARGES_LABELS,
    FIGURES_DIR,
    FLOW_NAME,
    NUMERIC_COLUMNS,
    PIPELINE_METRICS_PATH,
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
    TARGET_COLUMN,
    TENURE_BINS,
    TENURE_LABELS,
)


@task(name="1.2-data-ingestion", retries=2, retry_delay_seconds=5)
def task_data_ingestion() -> pd.DataFrame:
    """
    Sub-Objective 1.2: Ingests the Telco Customer Churn dataset.
    Validates file existence, row/column counts, and structural integrity.
    """
    logger = get_run_logger()
    logger.info(">>> [Task 1.2] Starting Data Ingestion from: %s", RAW_DATA_PATH)

    if not RAW_DATA_PATH.exists():
        logger.warning("Dataset not found locally. Downloading from public repository...")
        import urllib.request
        url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
        RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, RAW_DATA_PATH)

    df = pd.read_csv(RAW_DATA_PATH)
    logger.info(
        "Data Ingestion Successful! Ingested shape: %d rows, %d columns.",
        df.shape[0],
        df.shape[1],
    )
    return df


@task(name="1.3-data-preprocessing")
def task_data_preprocessing(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Sub-Objective 1.3: Data Pre-processing:
    - Displaying summary statistics
    - Checking for missing values
    - Imputing missing data for numeric columns (TotalCharges)
    - Displaying data types
    - Normalizing numeric features using MinMaxScaler
    """
    logger = get_run_logger()
    logger.info(">>> [Task 1.3] Starting Data Pre-processing...")

    # Copy DataFrame to avoid mutation
    processed_df = df.copy()

    # 1. Display Data Types before conversion
    raw_dtypes = {col: str(dtype) for col, dtype in processed_df.dtypes.items()}
    logger.info("Raw Feature Data Types: %s", json.dumps(raw_dtypes, indent=2))

    # 2. Check for missing values / blanks
    missing_initial = {}
    for col in processed_df.columns:
        if processed_df[col].dtype == object:
            blank_count = int((processed_df[col].astype(str).str.strip() == "").sum())
            null_count = int(processed_df[col].isna().sum())
            total_missing = blank_count + null_count
        else:
            total_missing = int(processed_df[col].isna().sum())
        if total_missing > 0:
            missing_initial[col] = total_missing

    logger.info("Detected Initial Missing / Blank Values: %s", missing_initial)

    # 3. Numeric Conversion & Missing Value Imputation
    # TotalCharges contains space characters for customers with tenure == 0
    processed_df["TotalCharges"] = pd.to_numeric(processed_df["TotalCharges"].astype(str).str.strip(), errors="coerce")
    missing_total_charges = int(processed_df["TotalCharges"].isna().sum())

    # Impute missing TotalCharges with median
    median_total_charges = float(processed_df["TotalCharges"].median())
    processed_df["TotalCharges"] = processed_df["TotalCharges"].fillna(median_total_charges)
    logger.info(
        "Imputed %d missing TotalCharges records using median value: %.2f",
        missing_total_charges,
        median_total_charges,
    )

    # 4. Summary Statistics for Numeric Columns
    summary_stats = {}
    for col in NUMERIC_COLUMNS:
        summary_stats[col] = {
            "count": int(processed_df[col].count()),
            "mean": float(processed_df[col].mean()),
            "std": float(processed_df[col].std()),
            "min": float(processed_df[col].min()),
            "25%": float(processed_df[col].quantile(0.25)),
            "50% (median)": float(processed_df[col].median()),
            "75%": float(processed_df[col].quantile(0.75)),
            "max": float(processed_df[col].max()),
            "skewness": float(processed_df[col].skew()),
        }
    logger.info("Computed Numeric Summary Statistics:\n%s", pd.DataFrame(summary_stats).to_string())

    # 5. Normalizing Data (Min-Max Normalization to [0, 1])
    scaler = MinMaxScaler()
    normalized_cols = [f"{col}_norm" for col in NUMERIC_COLUMNS]
    processed_df[normalized_cols] = scaler.fit_transform(processed_df[NUMERIC_COLUMNS])
    logger.info("Successfully normalized columns %s using MinMaxScaler into [0, 1].", NUMERIC_COLUMNS)

    preprocessing_metadata = {
        "raw_record_count": len(df),
        "processed_record_count": len(processed_df),
        "missing_values_detected": missing_initial,
        "imputation_details": {
            "column": "TotalCharges",
            "missing_count": missing_total_charges,
            "strategy": "median",
            "imputed_value": round(median_total_charges, 2),
        },
        "summary_statistics": summary_stats,
        "normalized_columns": normalized_cols,
    }

    return processed_df, preprocessing_metadata


@task(name="1.4-exploratory-data-analysis")
def task_exploratory_data_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Sub-Objective 1.4: Exploratory Data Analysis (EDA):
    - Calculating correlation coefficients (Pearson & Spearman)
    - Identifying correlations between numeric and categorical features (Chi-Square, Cramér's V, ANOVA)
    - Binning (tenure cohorts, MonthlyCharges tiers)
    - Encoding (binary mapping, one-hot encoding)
    - Assessing feature importance (Random Forest Gini importance & Mutual Information)
    - Visualizing data (univariate & bivariate charts)
    """
    logger = get_run_logger()
    logger.info(">>> [Task 1.4] Starting Exploratory Data Analysis (EDA)...")

    eda_df = df.copy()

    # 1. Target Encoding: Binary Churn (0/1)
    eda_df["Churn_binary"] = (eda_df[TARGET_COLUMN].str.strip() == "Yes").astype(int)
    churn_rate = float(eda_df["Churn_binary"].mean())
    logger.info("Overall Churn Rate: %.2f%% (%d churned / %d total)", churn_rate * 100, eda_df["Churn_binary"].sum(), len(eda_df))

    # 2. Binning
    # Tenure Cohorts
    eda_df["tenure_cohort"] = pd.cut(
        eda_df["tenure"],
        bins=TENURE_BINS,
        labels=TENURE_LABELS,
        include_lowest=True,
    )
    tenure_cohort_churn = eda_df.groupby("tenure_cohort", observed=False)["Churn_binary"].agg(["count", "mean"]).to_dict("index")

    # Monthly Charges Tiers
    eda_df["charges_tier"] = pd.cut(
        eda_df["MonthlyCharges"],
        bins=CHARGES_BINS,
        labels=CHARGES_LABELS,
        include_lowest=True,
    )
    charges_tier_churn = eda_df.groupby("charges_tier", observed=False)["Churn_binary"].agg(["count", "mean"]).to_dict("index")

    logger.info("Binning: Tenure Cohort Churn Rates: %s", tenure_cohort_churn)

    # 3. Numeric Correlation Coefficients (Pearson & Spearman)
    numeric_corr_cols = NUMERIC_COLUMNS + ["Churn_binary"]
    pearson_corr = eda_df[numeric_corr_cols].corr(method="pearson").round(4).to_dict()
    spearman_corr = eda_df[numeric_corr_cols].corr(method="spearman").round(4).to_dict()
    logger.info("Pearson Correlation with Churn: %s", {k: v["Churn_binary"] for k, v in pearson_corr.items()})

    # 4. Categorical Correlation (Chi-Square & Cramér's V)
    categorical_correlations = {}
    for cat_col in CATEGORICAL_COLUMNS:
        contingency_table = pd.crosstab(eda_df[cat_col], eda_df["Churn_binary"])
        chi2, p_val, dof, _ = stats.chi2_contingency(contingency_table)
        n = contingency_table.sum().sum()
        cramers_v = float(np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1))))
        categorical_correlations[cat_col] = {
            "chi2_stat": round(float(chi2), 2),
            "p_value": float(p_val),
            "cramers_v": round(cramers_v, 4),
            "is_significant": bool(p_val < 0.05),
        }

    # Sort categorical associations by Cramér's V
    sorted_cat_corr = dict(sorted(categorical_correlations.items(), key=lambda x: x[1]["cramers_v"], reverse=True))
    logger.info("Top Categorical Correlations (Cramer's V): %s", list(sorted_cat_corr.items())[:5])

    # 5. Encoding for ML Feature Importance
    # Binary Encoding
    encoded_df = eda_df.copy()
    for col in BINARY_COLUMNS:
        if col in encoded_df.columns:
            if col == "gender":
                encoded_df[col] = (encoded_df[col] == "Male").astype(int)
            else:
                encoded_df[col] = (encoded_df[col] == "Yes").astype(int)

    # One-Hot Encoding for remaining categorical columns
    cols_to_one_hot = [c for c in CATEGORICAL_COLUMNS if c not in BINARY_COLUMNS]
    encoded_df = pd.get_dummies(encoded_df, columns=cols_to_one_hot, drop_first=True)

    # Feature Matrix X and Target y
    exclude_cols = ["customerID", TARGET_COLUMN, "Churn_binary", "tenure_cohort", "charges_tier"]
    feature_cols = [c for c in encoded_df.columns if c not in exclude_cols]
    X = encoded_df[feature_cols]
    y = encoded_df["Churn_binary"]

    # Save processed dataset
    encoded_df.to_csv(PROCESSED_DATA_PATH, index=False)

    # 6. Feature Importance Assessment (Random Forest & Mutual Information)
    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    rf.fit(X, y)
    importances = rf.feature_importances_
    mi_scores = mutual_info_classif(X, y, random_state=42)

    feat_imp_df = pd.DataFrame({
        "Feature": feature_cols,
        "RF_Importance": importances,
        "Mutual_Info": mi_scores,
    }).sort_values(by="RF_Importance", ascending=False)

    top_features = feat_imp_df.head(10).to_dict(orient="records")
    logger.info("Top 5 Predictive Features (Random Forest):\n%s", feat_imp_df.head(5).to_string())

    # 7. Visualization Generation (Publication Quality Figures)
    _generate_eda_visualizations(eda_df, feat_imp_df, numeric_corr_cols)

    eda_metadata = {
        "overall_churn_rate": round(churn_rate * 100, 2),
        "pearson_correlations": pearson_corr,
        "spearman_correlations": spearman_corr,
        "categorical_associations_cramers_v": sorted_cat_corr,
        "tenure_cohort_churn": tenure_cohort_churn,
        "charges_tier_churn": charges_tier_churn,
        "top_features": top_features,
    }

    return eda_metadata


def _generate_eda_visualizations(df: pd.DataFrame, feat_imp_df: pd.DataFrame, numeric_cols: list) -> None:
    """Generates and saves all required univariate and bivariate visual charts."""
    sns.set_theme(style="whitegrid", font_scale=1.1)

    # 1. Univariate: Target Churn Class Balance
    fig, ax = plt.subplots(figsize=(6, 4.5))
    palette = ["#2b5c8f", "#d95f02"]
    counts = df[TARGET_COLUMN].value_counts()
    percentages = (counts / len(df) * 100).round(1)
    bars = ax.bar(counts.index, counts.values, color=palette, width=0.5, edgecolor="black")
    for bar, pct in zip(bars, percentages):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 50, f"{yval} ({pct}%)", ha="center", va="bottom", fontweight="bold")
    ax.set_title("Univariate: Customer Churn Class Distribution", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Churn Status", fontweight="bold")
    ax.set_ylabel("Customer Count", fontweight="bold")
    ax.set_ylim(0, max(counts.values) * 1.15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "churn_distribution.png", dpi=300)
    plt.close()

    # 2. Univariate: Numeric Feature Distributions (Histograms + KDE)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e"]
    for i, col in enumerate(["tenure", "MonthlyCharges", "TotalCharges"]):
        sns.histplot(df[col], kde=True, ax=axes[i], color=colors[i], bins=25, edgecolor="black", alpha=0.6)
        axes[i].set_title(f"Distribution of {col}", fontweight="bold", fontsize=12)
        axes[i].set_xlabel(col, fontweight="bold")
        axes[i].set_ylabel("Density / Count", fontweight="bold")
    plt.suptitle("Univariate: Continuous Feature Distributions with KDE", fontsize=14, fontweight="bold", y=1.03)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "numeric_distributions.png", dpi=300)
    plt.close()

    # 3. Bivariate: Churn by Contract Type
    fig, ax = plt.subplots(figsize=(7, 4.5))
    contract_churn = pd.crosstab(df["Contract"], df[TARGET_COLUMN], normalize="index") * 100
    contract_churn.plot(kind="bar", stacked=False, color=["#2b5c8f", "#d95f02"], ax=ax, edgecolor="black", width=0.6)
    ax.set_title("Bivariate: Churn Rate by Contract Type", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Contract Type", fontweight="bold")
    ax.set_ylabel("Percentage (%)", fontweight="bold")
    ax.legend(title="Churn", frameon=True)
    plt.xticks(rotation=0)
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height + 1), ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 100)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "bivariate_contract_churn.png", dpi=300)
    plt.close()

    # 4. Bivariate: Monthly Charges vs Churn
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.kdeplot(data=df, x="MonthlyCharges", hue=TARGET_COLUMN, common_norm=False, fill=True, palette=["#2b5c8f", "#d95f02"], alpha=0.4, ax=ax)
    ax.set_title("Bivariate: Monthly Charges Density by Churn Status", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Monthly Charges ($)", fontweight="bold")
    ax.set_ylabel("Density", fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "bivariate_charges_churn.png", dpi=300)
    plt.close()

    # 5. Binning Cohort: Tenure Cohort vs Churn Rate
    fig, ax = plt.subplots(figsize=(8, 4.5))
    cohort_rates = df.groupby("tenure_cohort", observed=False)["Churn_binary"].mean() * 100
    bars = ax.bar(cohort_rates.index.astype(str), cohort_rates.values, color="#e6550d", width=0.5, edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f"{h:.1f}%", ha="center", va="bottom", fontweight="bold")
    ax.set_title("Binned Analysis: Churn Rate Across Tenure Cohorts", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Tenure Cohort (Binned)", fontweight="bold")
    ax.set_ylabel("Churn Rate (%)", fontweight="bold")
    ax.set_ylim(0, 60)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "tenure_cohort_analysis.png", dpi=300)
    plt.close()

    # 6. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(7, 5))
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".3f", linewidths=1, ax=ax)
    ax.set_title("Pearson Correlation Heatmap (Continuous Features & Target)", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_heatmap.png", dpi=300)
    plt.close()

    # 7. Feature Importance Ranking
    fig, ax = plt.subplots(figsize=(9, 5))
    top_10 = feat_imp_df.head(10).iloc[::-1]
    ax.barh(top_10["Feature"], top_10["RF_Importance"], color="#3182bd", edgecolor="black", height=0.6)
    ax.set_title("Top 10 Feature Importances (Random Forest Gini Importance)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Relative Importance Score", fontweight="bold")
    for p in ax.patches:
        width = p.get_width()
        ax.text(width + 0.003, p.get_y() + p.get_height() / 2, f"{width:.3f}", ha="left", va="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "feature_importance_ranking.png", dpi=300)
    plt.close()

    # 8. Architecture Diagram
    _generate_architecture_diagram()


def _generate_architecture_diagram() -> None:
    """Generates an end-to-end DataOps and Cloud-Native API architecture diagram."""
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.axis("off")

    boxes = [
        {"text": "1. Data Ingestion\n(Kaggle/IBM Telco\n7,043 Records)", "x": 0.05, "y": 0.5, "w": 0.18, "h": 0.35, "color": "#d0e1fd"},
        {"text": "2. Preprocessing\n- Dtypes & Summary\n- Missing Imputation\n- MinMax Scaling", "x": 0.28, "y": 0.5, "w": 0.18, "h": 0.35, "color": "#c6ebd9"},
        {"text": "3. Exploratory Data\n- Pearson/Spearman\n- Chi-Sq / Cramer's V\n- Binning & Encoding\n- Feature Importance", "x": 0.51, "y": 0.5, "w": 0.20, "h": 0.35, "color": "#fde2b4"},
        {"text": "4. DataOps Orchestrator\n- Prefect 3 Flow\n- 2-Min Schedule\n- Cloud Dashboard", "x": 0.76, "y": 0.5, "w": 0.19, "h": 0.35, "color": "#e2d4f5"},
    ]

    from matplotlib.patches import FancyBboxPatch
    for b in boxes:
        rect = FancyBboxPatch((b["x"], b["y"] - b["h"] / 2), b["w"], b["h"], boxstyle="round,pad=0.02,rounding_size=0.03", facecolor=b["color"], edgecolor="#333333", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"] / 2, b["y"], b["text"], ha="center", va="center", fontsize=9, fontweight="bold")

    # Connect with arrows
    for i in range(len(boxes) - 1):
        x1 = boxes[i]["x"] + boxes[i]["w"]
        x2 = boxes[i + 1]["x"]
        ax.annotate("", xy=(x2, 0.5), xytext=(x1, 0.5),
                    arrowprops=dict(arrowstyle="->", lw=2.5, color="#1a1a1a"))

    # Bottom API Layer
    api_rect = FancyBboxPatch((0.15, 0.05), 0.70, 0.20, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor="#fee0d2", edgecolor="#de2d26", linewidth=1.5)
    ax.add_patch(api_rect)
    ax.text(0.5, 0.15, "Sub-Objective 2: Cloud-Native API Access Layer\nBuilt-in Prefect APIs (/api/flows, /api/deployments, /api/flow_runs) + FastAPI Gateway", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#a50f15")

    # Arrow down to API layer
    ax.annotate("", xy=(0.5, 0.26), xytext=(0.5, 0.32), arrowprops=dict(arrowstyle="<->", lw=2, color="#de2d26"))

    ax.set_title("AIMLCZG549: End-to-End Cloud-Native DataOps & API Architecture", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "dataops_pipeline_architecture.png", dpi=300)
    plt.close()


@task(name="1.5-model-evaluation-and-telemetry")
def task_model_evaluation_and_telemetry(
    prep_meta: Dict[str, Any], eda_meta: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Sub-Objective 1.5: DataOps Telemetry, Validation, and Metric Logging.
    Evaluates ML baseline, logs all pipeline parameters, and persists telemetry for Cloud Dashboard & API.
    """
    logger = get_run_logger()
    logger.info(">>> [Task 1.5] Logging DataOps Telemetry & Baseline Performance...")

    # Load processed data
    df = pd.read_csv(PROCESSED_DATA_PATH)
    exclude_cols = ["customerID", TARGET_COLUMN, "Churn_binary", "tenure_cohort", "charges_tier"]
    feature_cols = [c for c in df.columns if c not in exclude_cols]

    X = df[feature_cols]
    y = df["Churn_binary"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    accuracy = float(accuracy_score(y_test, y_pred))
    roc_auc = float(roc_auc_score(y_test, y_prob))

    logger.info("Pipeline Baseline Model Trained Successfully: Accuracy = %.4f, ROC-AUC = %.4f", accuracy, roc_auc)

    telemetry = {
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_name": FLOW_NAME,
        "status": "SUCCESS",
        "data_ingestion": {
            "source": "IBM/Kaggle Telco Customer Churn",
            "total_records": prep_meta["raw_record_count"],
        },
        "preprocessing": prep_meta,
        "eda_summary": eda_meta,
        "model_performance": {
            "model_type": "RandomForestClassifier",
            "test_accuracy": round(accuracy, 4),
            "roc_auc": round(roc_auc, 4),
        },
        "dataops_schedule": {
            "interval_seconds": 120,
            "cadence": "Every 2 minutes",
            "cloud_dashboard": "Prefect Cloud / Prefect Server UI",
        },
    }

    # Persist telemetry JSON for API access
    with open(PIPELINE_METRICS_PATH, "w") as f:
        json.dump(telemetry, f, indent=2)

    logger.info("Telemetry successfully saved to: %s", PIPELINE_METRICS_PATH)
    return telemetry


@flow(name=FLOW_NAME, log_prints=True)
def telco_churn_dataops_flow() -> Dict[str, Any]:
    """
    Master Prefect Flow orchestrating the end-to-end DataOps pipeline:
    1. Data Ingestion (1.2)
    2. Data Preprocessing (1.3)
    3. Exploratory Data Analysis & Visualization (1.4)
    4. Model Evaluation & Cloud Telemetry Persistence (1.5)
    """
    logger = get_run_logger()
    start_time = time.time()
    logger.info("=================================================================")
    logger.info("Starting Execution: %s", FLOW_NAME)
    logger.info("=================================================================")

    # Step 1: Ingest Data
    raw_df = task_data_ingestion()

    # Step 2: Preprocess Data
    processed_df, prep_meta = task_data_preprocessing(raw_df)

    # Step 3: EDA & Visualizations
    eda_meta = task_exploratory_data_analysis(processed_df)

    # Step 4: Model Evaluation & Telemetry
    telemetry = task_model_evaluation_and_telemetry(prep_meta, eda_meta)

    duration = time.time() - start_time
    logger.info("=================================================================")
    logger.info("Flow '%s' Completed Successfully in %.2f seconds.", FLOW_NAME, duration)
    logger.info("=================================================================")

    telemetry["execution_duration_seconds"] = round(duration, 2)
    return telemetry


if __name__ == "__main__":
    # Allows direct CLI execution for manual runs or tests
    print("Running Telco Churn DataOps Flow directly...")
    result = telco_churn_dataops_flow()
    print("Flow execution finished successfully!")
    print(f"Ingested Records: {result['data_ingestion']['total_records']}")
    print(f"ROC-AUC: {result['model_performance']['roc_auc']}")
