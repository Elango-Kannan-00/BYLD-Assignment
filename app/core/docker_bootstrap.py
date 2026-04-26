from __future__ import annotations

import subprocess
import time

from sqlalchemy import create_engine, text

from app.core.config import get_settings


def wait_for_database(timeout_seconds: int = 60, interval_seconds: float = 2.0) -> None:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    engine = create_engine(settings.database_url, pool_pre_ping=True)
    deadline = time.monotonic() + timeout_seconds

    while True:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except Exception as exc:  # pragma: no cover - defensive startup guard
            if time.monotonic() >= deadline:
                raise RuntimeError("Database did not become ready in time") from exc
            time.sleep(interval_seconds)


def main() -> None:
    wait_for_database()
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    subprocess.run(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        check=True,
    )


if __name__ == "__main__":
    main()
