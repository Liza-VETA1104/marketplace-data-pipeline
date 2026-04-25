import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from logging_setup import setup_logging, get_logger
from api import fetch_data_with_retry
from validators import validate_record
from loaders import save_to_db
from db import get_connection, close_connection


# -----------------------
# DATE UTIL
# -----------------------

def get_yesterday_str() -> str:
    tz = ZoneInfo("Europe/Moscow")
    return (datetime.now(tz).date() - timedelta(days=1)).strftime("%Y-%m-%d")


# -----------------------
# ETL CORE
# -----------------------

def load_date(conn, date_str: str):
    """Выполняет ETL для одной даты, используя переданное соединение"""
    raw_data = fetch_data_with_retry(date_str)

    if raw_data is None:
        return {"status": "api_error", "total": 0, "valid": 0, "dropped": 0, "attempted": 0}

    if len(raw_data) == 0:
        return {"status": "empty", "total": 0, "valid": 0, "dropped": 0, "attempted": 0}

    valid_records = []
    dropped = 0

    for record in raw_data:
        cleaned = validate_record(record)
        if cleaned:
            valid_records.append(cleaned)
        else:
            dropped += 1

    if not valid_records:
        return {
            "status": "no_valid_data",
            "total": len(raw_data),
            "valid": 0,
            "dropped": dropped,
            "attempted": 0,
        }

    result = save_to_db(valid_records, date_str, conn)

    return {
        "status": result["status"],
        "total": len(raw_data),
        "valid": len(valid_records),
        "dropped": dropped,
        "attempted": result["attempted"],
        "error": result.get("error"),
    }


# -----------------------
# MAIN ORCHESTRATOR
# -----------------------

def main():
    setup_logging()
    logger = get_logger(__name__)

    date = get_yesterday_str()

    logger.info("ETL start | date=%s", date)

    conn = get_connection()
    try:
        result = load_date(conn, date)

        logger.info(
            "ETL done | date=%s status=%s total=%d valid=%d dropped=%d attempted=%d%s",
            date,
            result["status"],
            result["total"],
            result["valid"],
            result["dropped"],
            result["attempted"],
            f" error={result['error']}" if result.get("error") else "",
        )

        if result["status"] not in ("ok", "empty"):
            sys.exit(1)

    finally:
        close_connection(conn)


# -----------------------
# ENTRYPOINT
# -----------------------

if __name__ == "__main__":
    main()