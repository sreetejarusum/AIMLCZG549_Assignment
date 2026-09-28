"""
Presentation Video Generator for AIMLCZG549 Assignment 1.

Features:
- Indian English Male Voice narration using macOS 'Rishi' (en_IN) text-to-speech.
- Follows the exact script from video_presentation_script.md for SREE TEJA R (100% solo).
- High-Definition 1080p (1920x1080) slide generation with embedded figures and screenshots.
- Assembles video segments with FFmpeg into AIMLCZG549_Assignment1_Video_Walkthrough.mp4.
"""

import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image

import imageio_ffmpeg

from AIMLCZG549_Assignment1.src.config import (
    FIGURES_DIR,
    PROJECT_ROOT,
    SCREENSHOTS_DIR,
)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
TEMP_VIDEO_DIR = PROJECT_ROOT / ".video_temp"
OUTPUT_VIDEO_PATH = PROJECT_ROOT / "AIMLCZG549_Assignment1_Video_Walkthrough.mp4"


def setup_temp_dir():
    if TEMP_VIDEO_DIR.exists():
        shutil.rmtree(TEMP_VIDEO_DIR)
    TEMP_VIDEO_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------
# 1. Slide Rendering (1920 x 1080 Full HD)
# -------------------------------------------------------------
def render_slide_1(output_path: Path):
    """Slide 1: Project Title, Overview, and Architecture Flowchart."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor("#0b132b")
    ax.set_facecolor("#0b132b")
    ax.axis("off")

    # Header Banner
    header = FancyBboxPatch((0.03, 0.85), 0.94, 0.12, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=2)
    ax.add_patch(header)
    ax.text(0.05, 0.925, "AIMLCZG549 - API-DRIVEN CLOUD NATIVE SOLUTIONS", color="#48cae4", fontsize=16, fontweight="bold")
    ax.text(0.05, 0.875, "Assignment I: Cloud-Based Data Science Pipeline & API-Driven Architecture", color="#ffffff", fontsize=14, fontweight="bold")
    ax.text(0.72, 0.90, "GROUP ID: 80 | SREE TEJA R (100%)", color="#00b4d8", fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#0b132b", edgecolor="#00b4d8"))

    # Left Card: Metadata & Context
    left_card = FancyBboxPatch((0.03, 0.08), 0.38, 0.74, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(left_card)
    ax.text(0.05, 0.76, "PROJECT OVERVIEW", color="#90e0ef", fontsize=13, fontweight="bold")
    
    bullets = [
        "● Domain: Customer Churn Prevention in Telecom/SaaS",
        "● Business Problem: High subscriber acquisition costs (5x-7x retention)",
        "● Key Goals: Early churn prediction & driver identification",
        "--------------------------------------------------",
        "SUB-OBJECTIVE 1: DATA PIPELINE (10 Marks)",
        "  ▸ Ingestion: IBM/Kaggle Dataset (7,043 Records)",
        "  ▸ Preprocessing: Missing Imputation & Normalization",
        "  ▸ EDA: Pearson/Cramér's V, Binning, Feature Importance",
        "  ▸ DataOps: Prefect 3 Flow on a 2-Minute Schedule",
        "--------------------------------------------------",
        "SUB-OBJECTIVE 2: API ACCESS (5 Marks)",
        "  ▸ Built-in APIs: Flow, Deployment & Run Telemetry",
        "  ▸ Display 4 Details via GET /api/v1/application/details",
        "  ▸ Full Testing: HTTP 200, 202, 404, 422 Verified",
    ]
    for i, line in enumerate(bullets):
        color = "#ffffff" if "SUB-OBJECTIVE" in line else ("#48cae4" if "●" in line else "#cbd5e1")
        weight = "bold" if "SUB-OBJECTIVE" in line or "●" in line else "normal"
        ax.text(0.05, 0.71 - i * 0.045, line, color=color, fontsize=10, fontweight=weight)

    # Right Card: Architecture Diagram
    right_card = FancyBboxPatch((0.44, 0.08), 0.53, 0.74, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(right_card)
    ax.text(0.46, 0.76, "SYSTEM ARCHITECTURE FLOWCHART", color="#90e0ef", fontsize=13, fontweight="bold")

    arch_img_path = FIGURES_DIR / "dataops_pipeline_architecture.png"
    if arch_img_path.exists():
        img = Image.open(arch_img_path)
        # Position image in right card
        new_ax = fig.add_axes([0.45, 0.12, 0.51, 0.58])
        new_ax.imshow(img)
        new_ax.axis("off")

    plt.savefig(output_path, dpi=120)
    plt.close()


def render_slide_2(output_path: Path):
    """Slide 2: Data Ingestion & Pre-processing (1.2 & 1.3)."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor("#0b132b")
    ax.set_facecolor("#0b132b")
    ax.axis("off")

    # Header
    header = FancyBboxPatch((0.03, 0.85), 0.94, 0.12, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=2)
    ax.add_patch(header)
    ax.text(0.05, 0.925, "SUB-OBJECTIVE 1: DATA PIPELINE", color="#48cae4", fontsize=15, fontweight="bold")
    ax.text(0.05, 0.875, "Activities 1.2 & 1.3: Data Ingestion, Profiling, Imputation & Normalization", color="#ffffff", fontsize=13, fontweight="bold")
    ax.text(0.78, 0.90, "STAGE 1 & 2 / 5", color="#00b4d8", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#0b132b", edgecolor="#00b4d8"))

    # Card 1: Data Ingestion (1.2)
    c1 = FancyBboxPatch((0.03, 0.48), 0.45, 0.34, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(c1)
    ax.text(0.05, 0.77, "ACTIVITY 1.2: DATA INGESTION", color="#90e0ef", fontsize=12, fontweight="bold")
    c1_text = [
        "● Source: IBM / Kaggle Telco Customer Churn Public Benchmark",
        "● Total Scale: 7,043 Customer Records, 21 Attributes",
        "● Data Quality & Sufficiency: Robust statistical power for ML",
        "● Implementation: Automated Prefect task '1.2-data-ingestion'",
        "● Integrity Checks: Automatic schema validation and download fallback",
    ]
    for i, t in enumerate(c1_text):
        ax.text(0.05, 0.72 - i * 0.05, t, color="#e2e8f0", fontsize=9.5)

    # Card 2: Preprocessing & Imputation (1.3)
    c2 = FancyBboxPatch((0.51, 0.48), 0.46, 0.34, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(c2)
    ax.text(0.53, 0.77, "ACTIVITY 1.3: DATA PRE-PROCESSING", color="#90e0ef", fontsize=12, fontweight="bold")
    c2_text = [
        "1. Data Types Inspection: 17 Categorical, 3 Continuous, 1 ID",
        "2. Missing Detection: 11 Whitespace blanks in TotalCharges (tenure=0)",
        "3. Numeric Imputation: Coerced to float & imputed using Median ($1,397.47)",
        "4. Data Normalization: MinMaxScaler maps features strictly onto [0, 1]",
        "5. Automated Execution: Prefect Task '1.3-data-preprocessing'",
    ]
    for i, t in enumerate(c2_text):
        ax.text(0.53, 0.72 - i * 0.05, t, color="#e2e8f0", fontsize=9.5)

    # Bottom Card: Embedded Numeric Distribution Plot
    c3 = FancyBboxPatch((0.03, 0.05), 0.94, 0.39, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(c3)
    ax.text(0.05, 0.39, "NUMERIC DISTRIBUTIONS & SUMMARY STATISTICS (tenure, MonthlyCharges, TotalCharges)", color="#90e0ef", fontsize=11, fontweight="bold")

    num_img = FIGURES_DIR / "numeric_distributions.png"
    if num_img.exists():
        img = Image.open(num_img)
        new_ax = fig.add_axes([0.05, 0.07, 0.90, 0.30])
        new_ax.imshow(img)
        new_ax.axis("off")

    plt.savefig(output_path, dpi=120)
    plt.close()


def render_slide_3(output_path: Path):
    """Slide 3: Exploratory Data Analysis & Visualizations (1.4)."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor("#0b132b")
    ax.set_facecolor("#0b132b")
    ax.axis("off")

    # Header
    header = FancyBboxPatch((0.03, 0.85), 0.94, 0.12, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=2)
    ax.add_patch(header)
    ax.text(0.05, 0.925, "SUB-OBJECTIVE 1: DATA PIPELINE", color="#48cae4", fontsize=15, fontweight="bold")
    ax.text(0.05, 0.875, "Activity 1.4: Exploratory Data Analysis (EDA), Binning, Correlations & Plots", color="#ffffff", fontsize=13, fontweight="bold")
    ax.text(0.78, 0.90, "STAGE 3 / 5", color="#00b4d8", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#0b132b", edgecolor="#00b4d8"))

    # Top Key Stats Card
    stats_card = FancyBboxPatch((0.03, 0.69), 0.94, 0.13, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(stats_card)
    ax.text(0.05, 0.77, "KEY STATISTICAL FINDINGS:", color="#90e0ef", fontsize=11, fontweight="bold")
    findings = (
        "● Baseline Churn Rate: 26.54% (1,869 Churned / 7,043 Total)   |   "
        "● Top Cramer's V: Contract (0.4101), OnlineSecurity (0.3474), TechSupport (0.3429)\n"
        "● Pearson Correlation with Churn: tenure (-0.352), MonthlyCharges (+0.193)   |   "
        "● Tenure Cohort Churn: New (0-12m) = 47.4% vs Loyal (49-72m) = 9.5%"
    )
    ax.text(0.05, 0.72, findings, color="#ffffff", fontsize=9.5, linespacing=1.4)

    # 4 Quadrants for Figures
    fig_positions = [
        ("churn_distribution.png", [0.03, 0.05, 0.22, 0.60], "Target Class Balance"),
        ("bivariate_contract_churn.png", [0.27, 0.05, 0.23, 0.60], "Churn by Contract"),
        ("tenure_cohort_analysis.png", [0.52, 0.05, 0.23, 0.60], "Tenure Cohorts Binning"),
        ("correlation_heatmap.png", [0.76, 0.05, 0.21, 0.60], "Pearson Correlation Heatmap"),
    ]

    for fname, pos, label in fig_positions:
        fpath = FIGURES_DIR / fname
        if fpath.exists():
            img = Image.open(fpath)
            new_ax = fig.add_axes(pos)
            new_ax.imshow(img)
            new_ax.axis("off")

    plt.savefig(output_path, dpi=120)
    plt.close()


def render_slide_4(output_path: Path):
    """Slide 4: Feature Importance & DataOps 2-Minute Automation (1.5)."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor("#0b132b")
    ax.set_facecolor("#0b132b")
    ax.axis("off")

    # Header
    header = FancyBboxPatch((0.03, 0.85), 0.94, 0.12, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=2)
    ax.add_patch(header)
    ax.text(0.05, 0.925, "SUB-OBJECTIVE 1: DATA PIPELINE", color="#48cae4", fontsize=15, fontweight="bold")
    ax.text(0.05, 0.875, "Activities 1.4 & 1.5: Feature Importance & Prefect 2-Minute Scheduled DataOps", color="#ffffff", fontsize=13, fontweight="bold")
    ax.text(0.78, 0.90, "STAGE 4 / 5", color="#00b4d8", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#0b132b", edgecolor="#00b4d8"))

    # Left: Feature Importance
    c_left = FancyBboxPatch((0.03, 0.05), 0.45, 0.77, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(c_left)
    ax.text(0.05, 0.77, "FEATURE IMPORTANCE (Random Forest & Mutual Info)", color="#90e0ef", fontsize=12, fontweight="bold")

    feat_img = FIGURES_DIR / "feature_importance_ranking.png"
    if feat_img.exists():
        img = Image.open(feat_img)
        new_ax = fig.add_axes([0.04, 0.08, 0.43, 0.65])
        new_ax.imshow(img)
        new_ax.axis("off")

    # Right: Prefect Cloud Dashboard Screenshot
    c_right = FancyBboxPatch((0.51, 0.05), 0.46, 0.77, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(c_right)
    ax.text(0.53, 0.77, "ACTIVITY 1.5: PREFECT CLOUD DASHBOARD (2-Min Schedule)", color="#90e0ef", fontsize=12, fontweight="bold")

    dash_img = SCREENSHOTS_DIR / "01_prefect_cloud_dashboard.png"
    if dash_img.exists():
        img = Image.open(dash_img)
        new_ax = fig.add_axes([0.52, 0.08, 0.44, 0.65])
        new_ax.imshow(img)
        new_ax.axis("off")

    plt.savefig(output_path, dpi=120)
    plt.close()


def render_slide_5(output_path: Path):
    """Slide 5: Sub-Objective 2: API Access, Demonstration & Verification."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.patch.set_facecolor("#0b132b")
    ax.set_facecolor("#0b132b")
    ax.axis("off")

    # Header
    header = FancyBboxPatch((0.03, 0.85), 0.94, 0.12, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=2)
    ax.add_patch(header)
    ax.text(0.05, 0.925, "SUB-OBJECTIVE 2: API ACCESS", color="#48cae4", fontsize=15, fontweight="bold")
    ax.text(0.05, 0.875, "Activities 3.1, 3.2 & 3.3: Built-in APIs, 4 Application Details & HTTP Status Code Testing", color="#ffffff", fontsize=13, fontweight="bold")
    ax.text(0.78, 0.90, "STAGE 5 / 5", color="#00b4d8", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#0b132b", edgecolor="#00b4d8"))

    # Left: Postman Client Screenshot (HTTP 200 & 4 Details)
    c_left = FancyBboxPatch((0.03, 0.05), 0.46, 0.77, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(c_left)
    ax.text(0.05, 0.77, "POSTMAN API TESTING: 4 APPLICATION DETAILS (HTTP 200 OK)", color="#90e0ef", fontsize=11.5, fontweight="bold")

    postman_img = SCREENSHOTS_DIR / "03_postman_api_testing.png"
    if postman_img.exists():
        img = Image.open(postman_img)
        new_ax = fig.add_axes([0.04, 0.08, 0.44, 0.65])
        new_ax.imshow(img)
        new_ax.axis("off")

    # Right: Swagger UI & Status Code Verification (HTTP 200, 202, 404, 422)
    c_right = FancyBboxPatch((0.51, 0.05), 0.46, 0.77, boxstyle="round,pad=0.01", facecolor="#1c2541", edgecolor="#3a506b", linewidth=1.5)
    ax.add_patch(c_right)
    ax.text(0.53, 0.77, "STATUS CODE VERIFICATION (200, 202, 404, 422)", color="#90e0ef", fontsize=11.5, fontweight="bold")

    neg_img = SCREENSHOTS_DIR / "05_api_status_codes_verification.png"
    if neg_img.exists():
        img = Image.open(neg_img)
        new_ax = fig.add_axes([0.52, 0.08, 0.44, 0.65])
        new_ax.imshow(img)
        new_ax.axis("off")

    plt.savefig(output_path, dpi=120)
    plt.close()


# -------------------------------------------------------------
# 2. Audio Synthesis & Segment Compilation
# -------------------------------------------------------------
SEGMENTS = [
    {
        "id": 1,
        "title": "Segment 1: Project Introduction & Architecture",
        "text": (
            "Hello everyone and respected professors. Welcome to the demonstration of Assignment 1 for "
            "AIMLCZG549: API-driven Cloud Native Solutions, submitted under Group ID 80. "
            "My name is Sree Teja R (Student ID: 2025AE05629). I have developed an end-to-end, production-grade "
            "cloud-native Data Science and DataOps application addressing Customer Churn Prevention in Telecommunication "
            "and Subscription Platforms. "
            "In subscription industries, acquiring a new subscriber costs five to seven times more than retaining an existing customer. "
            "This project achieves two core sub-objectives: "
            "First, Sub-Objective 1: Building an automated DataOps pipeline orchestrating data ingestion, statistical data quality checks, "
            "missing value imputation, MinMax normalization, and exploratory analysis scheduled to run every two minutes using Prefect 3. "
            "Second, Sub-Objective 2: Providing cloud-native API access to internal flow definitions, deployments, execution telemetry, "
            "and real-time inference via a FastAPI gateway. "
            "Let us now dive into the Data Ingestion and Pre-processing implementation."
        ),
        "renderer": render_slide_1,
    },
    {
        "id": 2,
        "title": "Segment 2: Data Ingestion & Pre-processing",
        "text": (
            "Moving to Sub-Objective 1, Activities 1.2 and 1.3: "
            "For data ingestion, I sourced the IBM / Kaggle Telco Customer Churn dataset, comprising 7,043 customer accounts across 21 attributes. "
            "This volume provides high statistical power for modeling and hypothesis testing. "
            "During data profiling and preprocessing, five key activities were completed programmatically: "
            "1. Feature Data Types: Mapped 17 categorical features and 3 continuous variables: tenure, Monthly Charges, and Total Charges. "
            "2. Missing Value Detection: Identified 11 blank whitespace entries in TotalCharges corresponding to brand-new accounts with tenure equal to zero. "
            "3. Missing Data Imputation: Rather than discarding records, TotalCharges was coerced to numeric and imputed using the median value of "
            "1,397 dollars and 47 cents, maintaining statistical integrity. "
            "4. Summary Statistics: Computed parametric and non-parametric metrics including count, mean, standard deviation, quartiles, and skewness. "
            "5. Data Normalization: Applied MinMaxScaler to scale tenure, Monthly Charges, and Total Charges strictly into the interval 0 to 1, "
            "guaranteeing numerical stability for machine learning. "
            "Next, let us look at the Exploratory Data Analysis."
        ),
        "renderer": render_slide_2,
    },
    {
        "id": 3,
        "title": "Segment 3: Exploratory Data Analysis & Visualizations",
        "text": (
            "In Activity 1.4, I conducted thorough Exploratory Data Analysis across multiple dimensions: "
            "First, examining target class balance: our baseline churn rate is 26.54 percent, with 1,869 churned customers out of 7,043. "
            "Second, bivariate analysis revealed that Contract Type is the single strongest determinant of churn. Month-to-month subscribers "
            "experience an alarming 42.7 percent churn rate, compared to just 11.3 percent for one-year and 2.8 percent for two-year contracts. "
            "Third, Chi-Square tests of independence and Cramer's V statistics confirmed strong categorical associations for Contract, "
            "with Cramer's V equal to 0.4101, Online Security with 0.3474, and Tech Support with 0.3429. "
            "Fourth, I performed binning on customer tenure into four cohorts. Customers in their first year (0 to 12 months) churn at 47.4 percent, "
            "whereas loyal customers past 48 months churn at only 9.5 percent. "
            "Finally, Pearson and Spearman correlation matrices showed significant negative correlations between customer tenure and churn propensity. "
            "Let us now look at feature importance and our DataOps automation."
        ),
        "renderer": render_slide_3,
    },
    {
        "id": 4,
        "title": "Segment 4: Feature Importance & DataOps 2-Minute Scheduling",
        "text": (
            "Continuing in Activity 1.4, I encoded categorical features using binary mapping and One-Hot Encoding, and trained a Random Forest Classifier. "
            "Evaluating Gini importance and Mutual Information confirmed our top predictive churn drivers: tenure, Total Charges, Monthly Charges, "
            "Month-to-month contract, and Fiber Optic internet service. "
            "Moving to Activity 1.5 DataOps: "
            "The entire workflow is orchestrated using Prefect 3. Each stage—ingestion, preprocessing, EDA, and model evaluation—is a modular task "
            "with automated retry policies. "
            "I deployed the pipeline with an Interval Schedule of 120 seconds—exactly two minutes—as mandated by the assignment. "
            "As visible on the screen in our Prefect Cloud Dashboard, the pipeline triggers every two minutes automatically. All activity details, "
            "record counts, imputation statistics, and baseline ROC-AUC scores of 0.8245 are streamed live into the dashboard logs. "
            "Now, let us examine our API access and verification."
        ),
        "renderer": render_slide_4,
    },
    {
        "id": 5,
        "title": "Segment 5: Sub-Objective 2: API Access, Demonstration & Verification",
        "text": (
            "Under Sub-Objective 2: API Access, I implemented a robust dual API layer: "
            "First, in Activity 3.1, I utilized Prefect's Built-in Client APIs to programmatically retrieve flow definitions, deployments, "
            "and flow run execution states. "
            "Second, in Activity 3.2, I expose the four mandatory application details through our dedicated endpoint: GET /api/v1/application/details. "
            "As demonstrated in Postman, this endpoint returns: "
            "Detail 1: Flow Metadata: Flow Name 'telco-customer-churn-dataops-pipeline' and unique Flow ID. "
            "Detail 2: Deployment Config: Deployment Name, status READY, and the active two-minute schedule. "
            "Detail 3: Flow Run Telemetry: Latest Run 'pretty-jackal', status Completed, and 1.92 seconds duration. "
            "Detail 4: Pipeline Telemetry: 7,043 processed rows, 11 median-imputed values, and model ROC-AUC. "
            "Third, in Activity 3.3, I developed an automated test suite validating 12 test cases with strict HTTP status code verification: "
            "200 OK for successful data retrieval and real-time machine learning inference. "
            "202 ACCEPTED when triggering on-demand pipeline runs asynchronously. "
            "422 UNPROCESSABLE ENTITY when passing invalid customer schemas, demonstrating rigorous Pydantic validation. "
            "And 404 NOT FOUND for nonexistent resource routes. "
            "To conclude, this project bridges modern DataOps automation with cloud-native API microservices, fully satisfying every requirement "
            "of Assignment 1. Thank you for your time!"
        ),
        "renderer": render_slide_5,
    },
]


def build_full_presentation_video():
    setup_temp_dir()
    print("=" * 70)
    print("Starting Presentation Video Compilation (Indian English Male Voice: Rishi)")
    print("=" * 70)

    segment_video_files = []

    for seg in SEGMENTS:
        seg_id = seg["id"]
        print(f"\n--- Processing {seg['title']} ---")

        # 1. Render slide image
        slide_img = TEMP_VIDEO_DIR / f"slide_{seg_id}.png"
        seg["renderer"](slide_img)
        print(f"  [1/4] Slide {seg_id} rendered to: {slide_img.name}")

        # 2. Synthesize Audio via macOS Indian English Voice (Rishi)
        raw_aiff = TEMP_VIDEO_DIR / f"audio_{seg_id}.aiff"
        mp3_audio = TEMP_VIDEO_DIR / f"audio_{seg_id}.mp3"
        subprocess.run(["say", "-v", "Rishi", "-o", str(raw_aiff), seg["text"]], check=True)

        # Convert to MP3 using FFmpeg
        subprocess.run(
            [FFMPEG_EXE, "-y", "-i", str(raw_aiff), "-b:a", "192k", str(mp3_audio)],
            capture_output=True,
            check=True,
        )
        print(f"  [2/4] Voice audio synthesized: {mp3_audio.name}")

        # 3. Create Video Segment with Still Image and Audio
        seg_video = TEMP_VIDEO_DIR / f"segment_{seg_id}.mp4"
        cmd = [
            FFMPEG_EXE,
            "-y",
            "-loop", "1",
            "-i", str(slide_img),
            "-i", str(mp3_audio),
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(seg_video),
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"  [3/4] Video segment assembled: {seg_video.name}")
        segment_video_files.append(seg_video)

    # 4. Concatenate all segments into final MP4
    print("\n--- Concatenating all 5 segments into final video ---")
    concat_list_file = TEMP_VIDEO_DIR / "concat_list.txt"
    with open(concat_list_file, "w") as f:
        for vfile in segment_video_files:
            f.write(f"file '{vfile.resolve()}'\n")

    cmd_concat = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(OUTPUT_VIDEO_PATH),
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    file_size_mb = OUTPUT_VIDEO_PATH.stat().st_size / (1024 * 1024)
    print("=" * 70)
    print(f"Presentation Video generated successfully!")
    print(f"Output File: {OUTPUT_VIDEO_PATH}")
    print(f"Size: {file_size_mb:.2f} MB")
    print("=" * 70)

    # Cleanup temp directory
    shutil.rmtree(TEMP_VIDEO_DIR, ignore_errors=True)
    return OUTPUT_VIDEO_PATH


if __name__ == "__main__":
    build_full_presentation_video()
