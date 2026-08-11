from config import get_configs
from connectors.postgres import PostgresConnector
from connectors.prometheus import PrometheusConnector
from langchain_core.tools import tool

_settings = get_configs()
_prometheus = PrometheusConnector(_settings)
_postgres = PostgresConnector(_settings)

MAX_SERIES = 15
MAX_QUERY_TEXT_CHARS = 300


@tool
def prometheus_targets_up() -> dict:
    """Return the up/down status of every Prometheus scrape target."""
    return _prometheus.targets_up()


@tool
def prometheus_query(promql: str) -> dict:
    """Run an instant PromQL query against Prometheus. Returns at most 15 simplified
    series (metric labels + latest value) — NOT the raw API response, to keep results
    small. Prefer aggregated queries over raw ones, e.g.
    'sum(rate(container_cpu_usage_seconds_total[5m])) by (name)' instead of the bare
    metric name, which can return hundreds of series and blow the context budget.
    Other useful metrics: container_memory_usage_bytes, node_memory_MemAvailable_bytes,
    rate(node_cpu_seconds_total[5m])."""
    raw = _prometheus.query(promql)
    series = raw.get("data", {}).get("result", [])
    trimmed = series[:MAX_SERIES]
    simplified = [
        {"labels": s.get("metric", {}), "value": s.get("value", [None, None])[1]}
        for s in trimmed
    ]
    return {
        "series_returned": len(simplified),
        "series_total": len(series),
        "truncated": len(series) > MAX_SERIES,
        "results": simplified,
    }


@tool
def db_top_queries(limit: int = 5) -> list[dict]:
    """Return the top N most expensive SQL queries by total execution time,
    from Postgres's pg_stat_statements. Query text is truncated to keep results small."""
    rows = _postgres.top_queries(limit=limit)
    for row in rows:
        text = row.get("query", "")
        if len(text) > MAX_QUERY_TEXT_CHARS:
            row["query"] = text[:MAX_QUERY_TEXT_CHARS] + "... [truncated]"
    return rows
