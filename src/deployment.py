"""
Prefect Deployment Module for AIMLCZG549 Assignment 1.

Automates Sub-Objective 1.5:
- Creates and registers the deployment with a recurring schedule of 2 minutes (120 seconds).
- Configures tags, parameters, and metadata for Cloud Dashboard and API visibility.
- Provides a CLI entrypoint to serve or trigger the scheduled pipeline runs.
"""

import asyncio
from datetime import timedelta
from typing import Dict, Any

from prefect.client.orchestration import get_client
from prefect.client.schemas.schedules import IntervalSchedule

from AIMLCZG549_Assignment1.src.config import (
    DEPLOYMENT_NAME,
    FLOW_NAME,
    SCHEDULE_INTERVAL_SECONDS,
)
from AIMLCZG549_Assignment1.src.pipeline import telco_churn_dataops_flow


async def register_deployment() -> str:
    """
    Registers the 2-minute recurring schedule deployment in the Prefect backend.
    """
    print(f"Creating deployment '{DEPLOYMENT_NAME}' with {SCHEDULE_INTERVAL_SECONDS}s (2-minute) interval...")

    # Build deployment using Prefect 3 to_deployment API
    deployment = await telco_churn_dataops_flow.to_deployment(
        name=DEPLOYMENT_NAME,
        interval=timedelta(seconds=SCHEDULE_INTERVAL_SECONDS),
        tags=["aimlczg549", "assignment1", "dataops", "churn-prediction", "2min-interval"],
        description=(
            "Automated DataOps pipeline executing data ingestion, preprocessing (missing imputation, normalization), "
            "and exploratory data analysis (correlations, binning, encoding, feature importance) every 2 minutes."
        ),
    )

    deployment_id = await deployment.apply()
    print(f"Deployment registered successfully! Deployment ID: {deployment_id}")
    return str(deployment_id)


async def get_deployment_info() -> Dict[str, Any]:
    """
    Retrieves deployment metadata via the Prefect Built-in API.
    """
    async with get_client() as client:
        deployments = await client.read_deployments()
        for dep in deployments:
            if dep.name == DEPLOYMENT_NAME:
                schedules_info = []
                for s in dep.schedules:
                    schedules_info.append({
                        "schedule_type": "Interval",
                        "interval_seconds": SCHEDULE_INTERVAL_SECONDS,
                        "cadence": "Every 2 minutes",
                        "active": s.active,
                        "raw_schedule": str(s.schedule),
                    })
                return {
                    "id": str(dep.id),
                    "name": dep.name,
                    "flow_id": str(dep.flow_id),
                    "status": "READY",
                    "tags": dep.tags,
                    "schedules": schedules_info,
                    "created": str(dep.created),
                    "updated": str(dep.updated),
                }
    return {}


def serve_deployment() -> None:
    """
    Starts an active Prefect runner serving the deployment.
    Executes the workflow every 2 minutes and streams logs live.
    """
    print(f"Starting Prefect Runner serving '{DEPLOYMENT_NAME}' every 2 minutes...")
    telco_churn_dataops_flow.serve(
        name=DEPLOYMENT_NAME,
        interval=SCHEDULE_INTERVAL_SECONDS,
        tags=["aimlczg549", "assignment1", "dataops"],
        description="2-minute recurring DataOps pipeline",
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        serve_deployment()
    else:
        dep_id = asyncio.run(register_deployment())
        info = asyncio.run(get_deployment_info())
        print("Deployment Metadata Retrieved via API:")
        import json
        print(json.dumps(info, indent=2))
