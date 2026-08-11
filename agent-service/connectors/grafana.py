import requests
from config import Config


class GrafanaConnector:
    def __init__(self, config: Config):
        self.base_url = config.grafana_url
        self._headers = {"Authorization": f"Bearer {config.grafana_api_key}"}

    def is_healthy(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/health", timeout=5)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def list_datasources(self) -> list[dict]:
        resp = requests.get(
            f"{self.base_url}/api/datasources", headers=self._headers, timeout=10
        )
        resp.raise_for_status()
        return resp.json()
