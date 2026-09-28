"""
Automated API Testing and Documentation Suite for AIMLCZG549 Assignment 1.

Fulfills Sub-Objective 3.3:
- Tests the APIs using an automated API client.
- Demonstrates successful requests and responses across all endpoints.
- Verifies appropriate HTTP status codes:
  * 200 OK (Data retrieval, Health, Inference)
  * 202 ACCEPTED (Asynchronous Pipeline Trigger)
  * 404 NOT FOUND (Resource absence handling)
  * 422 UNPROCESSABLE ENTITY (Pydantic schema validation error)
- Serializes verified sample request/response payloads to test_results/ for documentation and screenshots.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from fastapi.testclient import TestClient

from AIMLCZG549_Assignment1.src.api_service import app
from AIMLCZG549_Assignment1.src.config import TEST_RESULTS_DIR


def run_api_test_suite() -> Dict[str, Any]:
    """Executes exhaustive test suite against all API endpoints and logs results."""
    print("=" * 70)
    print("Starting Automated API Testing & Verification Suite (AIMLCZG549 Sub-Objective 3.3)")
    print("=" * 70)

    client = TestClient(app)
    test_results: List[Dict[str, Any]] = []

    # -------------------------------------------------------------
    # Test 1: Health Check (GET /health) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/health")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    test_1 = {
        "test_id": "TEST-01",
        "name": "System Health Check",
        "method": "GET",
        "endpoint": "/health",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_1)
    print(f"[{test_1['result']}] {test_1['method']} {test_1['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # -------------------------------------------------------------
    # Test 2: Display 4 Application Details (GET /api/v1/application/details) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/application/details")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    body = resp.json()
    assert "key_application_details" in body
    details = body["key_application_details"]
    assert "detail_1_flow_metadata" in details
    assert "detail_2_deployment_config" in details
    assert "detail_3_flow_run_telemetry" in details
    assert "detail_4_pipeline_and_model_metrics" in details

    test_2 = {
        "test_id": "TEST-02",
        "name": "Retrieve Key Application Details (4 Details)",
        "method": "GET",
        "endpoint": "/api/v1/application/details",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": body,
    }
    test_results.append(test_2)
    print(f"[{test_2['result']}] {test_2['method']} {test_2['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # Save to dedicated sample file
    with open(TEST_RESULTS_DIR / "sample_app_details_response.json", "w") as f:
        json.dump(body, f, indent=2)

    # -------------------------------------------------------------
    # Test 3: Prefect Flows Built-in API (GET /api/v1/prefect/flows) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/prefect/flows")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200
    test_3 = {
        "test_id": "TEST-03",
        "name": "Prefect Built-in Flow Information",
        "method": "GET",
        "endpoint": "/api/v1/prefect/flows",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_3)
    print(f"[{test_3['result']}] {test_3['method']} {test_3['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    with open(TEST_RESULTS_DIR / "sample_flow_response.json", "w") as f:
        json.dump(resp.json(), f, indent=2)

    # -------------------------------------------------------------
    # Test 4: Prefect Deployments Built-in API (GET /api/v1/prefect/deployments) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/prefect/deployments")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200
    test_4 = {
        "test_id": "TEST-04",
        "name": "Prefect Built-in Deployment & 2-Min Schedule",
        "method": "GET",
        "endpoint": "/api/v1/prefect/deployments",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_4)
    print(f"[{test_4['result']}] {test_4['method']} {test_4['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    with open(TEST_RESULTS_DIR / "sample_deployment_response.json", "w") as f:
        json.dump(resp.json(), f, indent=2)

    # -------------------------------------------------------------
    # Test 5: Prefect Flow Runs Built-in API (GET /api/v1/prefect/flow-runs) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/prefect/flow-runs")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200
    test_5 = {
        "test_id": "TEST-05",
        "name": "Prefect Built-in Flow Run Telemetry",
        "method": "GET",
        "endpoint": "/api/v1/prefect/flow-runs",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_5)
    print(f"[{test_5['result']}] {test_5['method']} {test_5['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    with open(TEST_RESULTS_DIR / "sample_flow_runs_response.json", "w") as f:
        json.dump(resp.json(), f, indent=2)

    # -------------------------------------------------------------
    # Test 6: Pipeline Telemetry & Quality Metrics (GET /api/v1/pipeline/metrics) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/pipeline/metrics")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200
    test_6 = {
        "test_id": "TEST-06",
        "name": "Pipeline Telemetry & Quality Metrics",
        "method": "GET",
        "endpoint": "/api/v1/pipeline/metrics",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_6)
    print(f"[{test_6['result']}] {test_6['method']} {test_6['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # -------------------------------------------------------------
    # Test 7: EDA Correlations (GET /api/v1/eda/correlations) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/eda/correlations")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200
    test_7 = {
        "test_id": "TEST-07",
        "name": "Exploratory Data Analysis Correlations",
        "method": "GET",
        "endpoint": "/api/v1/eda/correlations",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_7)
    print(f"[{test_7['result']}] {test_7['method']} {test_7['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # -------------------------------------------------------------
    # Test 8: Feature Importance (GET /api/v1/eda/feature-importance) -> Expect 200 OK
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/eda/feature-importance")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200
    test_8 = {
        "test_id": "TEST-08",
        "name": "Machine Learning Feature Importance Rankings",
        "method": "GET",
        "endpoint": "/api/v1/eda/feature-importance",
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_8)
    print(f"[{test_8['result']}] {test_8['method']} {test_8['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # -------------------------------------------------------------
    # Test 9: Real-time ML Churn Prediction (POST /api/v1/predict/churn) -> Expect 200 OK
    # -------------------------------------------------------------
    high_risk_customer = {
        "tenure": 2,
        "MonthlyCharges": 89.5,
        "TotalCharges": 179.0,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "PaymentMethod": "Electronic check",
        "OnlineSecurity": "No",
        "TechSupport": "No",
    }
    start = time.perf_counter()
    resp = client.post("/api/v1/predict/churn", json=high_risk_customer)
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 200
    body = resp.json()
    assert body["churn_prediction"] in ["Yes", "No"]
    test_9 = {
        "test_id": "TEST-09",
        "name": "Real-time Customer Churn Prediction Inference",
        "method": "POST",
        "endpoint": "/api/v1/predict/churn",
        "request_body": high_risk_customer,
        "expected_status": 200,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": body,
    }
    test_results.append(test_9)
    print(f"[{test_9['result']}] {test_9['method']} {test_9['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    with open(TEST_RESULTS_DIR / "sample_prediction_response.json", "w") as f:
        json.dump(body, f, indent=2)

    # -------------------------------------------------------------
    # Test 10: Trigger Pipeline Execution (POST /api/v1/pipeline/trigger) -> Expect 202 ACCEPTED
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.post("/api/v1/pipeline/trigger")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 202
    test_10 = {
        "test_id": "TEST-10",
        "name": "Asynchronous On-Demand Pipeline Trigger",
        "method": "POST",
        "endpoint": "/api/v1/pipeline/trigger",
        "expected_status": 202,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_10)
    print(f"[{test_10['result']}] {test_10['method']} {test_10['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # -------------------------------------------------------------
    # Test 11: Schema Validation Error (POST /api/v1/predict/churn with missing field) -> Expect 422 UNPROCESSABLE ENTITY
    # -------------------------------------------------------------
    invalid_customer = {
        "tenure": -5,  # Invalid: negative tenure violated ge=0 constraint
        "MonthlyCharges": "invalid-string",  # Invalid type
    }
    start = time.perf_counter()
    resp = client.post("/api/v1/predict/churn", json=invalid_customer)
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 422
    test_11 = {
        "test_id": "TEST-11",
        "name": "Pydantic Schema Validation Failure Handling",
        "method": "POST",
        "endpoint": "/api/v1/predict/churn",
        "request_body": invalid_customer,
        "expected_status": 422,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_11)
    print(f"[{test_11['result']}] {test_11['method']} {test_11['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # -------------------------------------------------------------
    # Test 12: Resource Not Found Simulation (GET /api/v1/resource/not-found) -> Expect 404 NOT FOUND
    # -------------------------------------------------------------
    start = time.perf_counter()
    resp = client.get("/api/v1/resource/not-found")
    latency = round((time.perf_counter() - start) * 1000, 2)
    assert resp.status_code == 404
    test_12 = {
        "test_id": "TEST-12",
        "name": "Resource Not Found Handling",
        "method": "GET",
        "endpoint": "/api/v1/resource/not-found",
        "expected_status": 404,
        "actual_status": resp.status_code,
        "latency_ms": latency,
        "result": "PASSED",
        "response_sample": resp.json(),
    }
    test_results.append(test_12)
    print(f"[{test_12['result']}] {test_12['method']} {test_12['endpoint']} -> HTTP {resp.status_code} ({latency} ms)")

    # Summary report
    summary = {
        "test_suite": "AIMLCZG549 Sub-Objective 3.3 Verification Suite",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_tests": len(test_results),
        "passed": sum(1 for t in test_results if t["result"] == "PASSED"),
        "failed": sum(1 for t in test_results if t["result"] == "FAILED"),
        "http_status_codes_verified": [200, 202, 404, 422],
        "test_cases": test_results,
    }

    with open(TEST_RESULTS_DIR / "api_test_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("=" * 70)
    print(f"API Testing Complete: {summary['passed']}/{summary['total_tests']} tests passed.")
    print(f"Results persisted to: {TEST_RESULTS_DIR / 'api_test_summary.json'}")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    run_api_test_suite()
