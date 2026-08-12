import sqlite3
import logging
from config import DB_TYPE, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, SQLITE_DB_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    """
    Centralized MySQL database connection function.
    Connects to MySQL server (host, port, user, password from .env, database: ai_career).
    If MySQL server is unavailable or fails, falls back smoothly to local SQLite database.
    """
    if DB_TYPE == "mysql":
        try:
            import mysql.connector
            from mysql.connector import Error

            conn = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                connection_timeout=10,
                autocommit=False
            )
            if conn.is_connected():
                logger.info(f"Successfully connected to MySQL database '{DB_NAME}' at {DB_HOST}:{DB_PORT}")
                return conn, "mysql"
        except Exception as e:
            logger.error(f"MySQL connection error ({DB_HOST}:{DB_PORT}/{DB_NAME}): {e}. Falling back to SQLite.")

    # Fallback to local SQLite DB if MySQL is unavailable
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(SQLITE_DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    logger.info(f"Using local SQLite database fallback at {SQLITE_DB_PATH}")
    return conn, "sqlite"

def close_connection(conn, cursor=None):
    """
    Properly closes cursor and database connection.
    """
    if cursor:
        try:
            cursor.close()
        except Exception as e:
            logger.debug(f"Error closing cursor: {e}")
    if conn:
        try:
            conn.close()
        except Exception as e:
            logger.debug(f"Error closing connection: {e}")

