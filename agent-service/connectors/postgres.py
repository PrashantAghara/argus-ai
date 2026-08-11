import psycopg2
from config import Config


class PostgresConnector:
    def __init__(self, config: Config):
        self.configs = {
            "host": config.postgres_host,
            "port": config.postgres_port,
            "dbname": config.postgres_db,
            "user": config.postgres_user,
            "password": config.postgres_password,
        }

    def _connect(self):
        return psycopg2.connect(**self.configs)

    def is_healthy(self) -> bool:
        try:
            with self._connect() as conn, conn.cursor() as cur:
                cur.execute("SELECT 1;")
                return cur.fetchone() == (1,)
        except psycopg2.Error:
            return False

    def top_queries(self, limit: int = 5) -> list[dict]:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT query, calls, total_exec_time, mean_exec_time
                FROM pg_stat_statements
                ORDER BY total_exec_time DESC
                LIMIT %s;
                """,
                (limit),
            )
            columns = ["query", "calls", "total_exec_time", "mean_exec_time"]
            return [dict(zip(columns, row)) for row in cur.fetchall()]

    def insert_embedding(self, summary: str, embedding: list[float]) -> None:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO incident_postmortems (summary, embedding) VALUES (%s, %s)",
                (summary, embedding),
            )
            conn.commit()

    def similar_incidents(self, embedding: list[float], limit: int = 3) -> list[dict]:
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    SELECT summary, embedding <-> %s AS distance
                    FROM incident_postmortems
                    ORDER BY distance
                    LIMIT %s;
                    """,
                (embedding, limit),
            )
            return [{"summary": row[0], "distance": row[1]} for row in cur.fetchall()]
