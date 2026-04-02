from app.db.connection import get_db_connection


def get_top_funded_startups(limit=10):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.name, f.funding_total_usd
        FROM startups s
        JOIN funding_profile f ON s.startup_id = f.startup_id
        WHERE f.funding_total_usd IS NOT NULL
        ORDER BY f.funding_total_usd DESC
        LIMIT %s;
    """, (limit,))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def get_startups_by_market(market_name, limit=10):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.name, m.market_name
        FROM markets m
        JOIN startups s ON s.market_id = m.market_id
        WHERE m.market_name = %s
        LIMIT %s;
    """, (market_name, limit))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def get_startups_by_country(country_code, limit=10):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.name, l.country_code
        FROM startups s
        JOIN locations l ON s.location_id = l.location_id
        WHERE l.country_code = %s
        LIMIT %s;
    """, (country_code, limit))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def get_venture_backed_startups(limit=10):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.name, f.venture
        FROM startups s
        JOIN funding_profile f ON s.startup_id = f.startup_id
        WHERE f.venture IS NOT NULL AND f.venture > 0
        ORDER BY f.venture DESC
        LIMIT %s;
    """, (limit,))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def get_competitors_by_market(market_name, limit=10):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.name, m.market_name, f.funding_total_usd
        FROM markets m
        JOIN startups s ON s.market_id = m.market_id
        JOIN funding_profile f ON s.startup_id = f.startup_id
        WHERE m.market_name = %s
        AND f.funding_total_usd IS NOT NULL
        ORDER BY f.funding_total_usd DESC
        LIMIT %s;
    """, (market_name, limit))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
