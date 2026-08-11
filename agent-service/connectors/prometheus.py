import requests
from config import Config


class PrometheusConnector:
    def __init__(self, config: Config):
        self.base_url = config.pprometheus_url

    def query(self, promql: str) -> dict:
        response = requests.get(
            f"{self.base_url}/api/v1/query", params={"query": promql}, timeout=10
        )
        response.raise_for_status()
        return response.json()

    def is_healthy(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/-/healthy", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def targets_up(self) -> dict:
        result = self.query("up")

        return {
            series["metric"]["job"]: series["value"][1]
            for series in result["data"]["result"]
        }
