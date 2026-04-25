from psycopg2.extras import execute_values
from psycopg2 import OperationalError, InterfaceError, DatabaseError
import time
from logging_setup import get_logger

logger = get_logger(__name__)


def save_to_db(records, date, conn, retries=3, delay=1):
    if not records:
        return {"attempted": 0, "status": "empty"}

    last_error = None

    for attempt in range(1, retries + 1):
        try:
            _save_to_db_impl(conn, records, date)
            return {"attempted": len(records), "status": "ok"}

        except (OperationalError, InterfaceError, DatabaseError) as e:
            last_error = e
            
            try:
                conn.rollback()
            except Exception:
                pass

            logger.error(
                "DB error | date=%s attempt=%d/%d error=%s",
                date, attempt, retries, e
            )

            if attempt < retries:
                time.sleep(min(delay * (2 ** (attempt - 1)), 10))

    logger.error("DB FINAL FAIL | date=%s error=%s", date, last_error)

    return {
        "attempted": len(records),
        "status": "failed",
        "error": str(last_error)
    }


def _save_to_db_impl(conn, records, date):
    """Pure insert layer"""
    with conn.cursor() as cur:
        values = [
            (
                r["client_id"],
                r["gender"],
                r["purchase_date"],
                r["purchase_time_seconds"],
                r["product_id"],
                r["quantity"],
                r["price_per_item"],
                r["discount_per_item"],
                r["total_price"],
            )
            for r in records
        ]

        query = """
            INSERT INTO sales (
                client_id, gender, purchase_date, purchase_time_seconds,
                product_id, quantity, price_per_item, discount_per_item, total_price
            )
            VALUES %s
            ON CONFLICT (client_id, product_id, purchase_date, purchase_time_seconds)
            DO NOTHING
        """

        execute_values(cur, query, values, page_size=1000)

    conn.commit()

    logger.info(
        "DB load | date=%s attempted=%d",
        date,
        len(records)
    )