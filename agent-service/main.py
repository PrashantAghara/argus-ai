from fastapi import FastAPI
from config import get_configs
from connectors.grafana import GrafanaConnector
from connectors.postgres import PostgresConnector
from connectors.prometheus import PrometheusConnector

app = FastAPI(title="Argus Agent Service")

configs = get_configs()
prometheus = PrometheusConnector(configs)
grafana = GrafanaConnector(configs)
postgres = PostgresConnector(configs)


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


@app.get("/agent/analyze")
def analyze():
    return {"status": "not_implemented", "note": "LangGraph agent graph comes next"}


def main():
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
