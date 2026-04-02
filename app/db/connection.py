import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """
    Returns a PostgreSQL database connection for the
    Startup Intelligence Database.
    """
    return psycopg2.connect(
        dbname="startup_intelligence_db",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )
