from agent.graph import graph
from config import get_configs
from connectors.grafana import GrafanaConnector
from connectors.postgres import PostgresConnector
from connectors.prometheus import PrometheusConnector
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Argus Agent Service")

configs = get_configs()
prometheus = PrometheusConnector(configs)
grafana = GrafanaConnector(configs)
postgres = PostgresConnector(configs)


class IncidentRequest(BaseModel):
    description: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/connectors")
def health_connectors():
    return {
        "prometheus": prometheus.is_healthy(),
        "grafana": grafana.is_healthy(),
        "postgres": postgres.is_healthy(),
    }


@app.post("/agent/analyze")
def analyze(request: IncidentRequest):
    result = graph.invoke({"incident_description": request.description})
    return {
        "relevant_agents": result.get("relevant_agents"),
        "apm_findings": result.get("apm_findings"),
        "db_findings": result.get("db_findings"),
        "infra_findings": result.get("infra_findings"),
        "final_report": result.get("final_report"),
    }


def main():
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
