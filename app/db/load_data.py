import pandas as pd
import psycopg2

# =========================
# PostgreSQL Connection
# =========================
conn = psycopg2.connect(
    dbname="startup_intelligence_db",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Reset tables before bulk loading to ensure repeatable, duplicate-free imports
# Reset tables before loading (makes script safe to rerun)
cur.execute("""
    TRUNCATE TABLE funding_profile, startups, markets, locations
    RESTART IDENTITY CASCADE;
""")
conn.commit()


# =========================
# Load cleaned dataset
# =========================
df = pd.read_csv("data/processed/cleaned_startup_investments.csv")

# Remove duplicate startups
df = df.drop_duplicates(subset=["permalink"])
# Fill missing values for text columns
text_columns = [
    "permalink", "name", "homepage_url", "category_list", "market",
    "status", "country_code", "state_code", "region", "city",
    "founded_quarter"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("")

# Convert date columns
date_columns = ["founded_at", "founded_month", "first_funding_at", "last_funding_at"]
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# =========================
# Insert Data Row by Row
# =========================
for _, row in df.iterrows():
    # Insert market
    cur.execute("""
        INSERT INTO markets (market_name, category_list)
        VALUES (%s, %s)
        RETURNING market_id
    """, (
        row["market"] if row["market"] != "" else None,
        row["category_list"] if row["category_list"] != "" else None
    ))
    market_id = cur.fetchone()[0]

    # Insert location
    cur.execute("""
        INSERT INTO locations (country_code, state_code, region, city)
        VALUES (%s, %s, %s, %s)
        RETURNING location_id
    """, (
        row["country_code"] if row["country_code"] != "" else None,
        row["state_code"] if row["state_code"] != "" else None,
        row["region"] if row["region"] != "" else None,
        row["city"] if row["city"] != "" else None
    ))
    location_id = cur.fetchone()[0]

    # Insert startup
    cur.execute("""
        INSERT INTO startups (
            permalink, name, homepage_url, status,
            founded_at, founded_month, founded_quarter, founded_year,
            market_id, location_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING startup_id
    """, (
        row["permalink"] if row["permalink"] != "" else None,
        row["name"],
        row["homepage_url"] if row["homepage_url"] != "" else None,
        row["status"] if row["status"] != "" else None,
        row["founded_at"].date() if pd.notna(row["founded_at"]) else None,
        row["founded_month"].date() if pd.notna(row["founded_month"]) else None,
        row["founded_quarter"] if row["founded_quarter"] != "" else None,
        int(row["founded_year"]) if pd.notna(row["founded_year"]) else None,
        market_id,
        location_id
    ))
    startup_id = cur.fetchone()[0]

    # Insert funding profile
    cur.execute("""
        INSERT INTO funding_profile (
            startup_id, funding_total_usd, funding_rounds,
            first_funding_at, last_funding_at,
            seed, venture, equity_crowdfunding, undisclosed,
            convertible_note, debt_financing, angel, grant_funding,
            private_equity, post_ipo_equity, post_ipo_debt,
            secondary_market, product_crowdfunding,
            round_A, round_B, round_C, round_D,
            round_E, round_F, round_G, round_H
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        startup_id,
        row["funding_total_usd"] if pd.notna(row["funding_total_usd"]) else None,
        int(row["funding_rounds"]) if pd.notna(row["funding_rounds"]) else None,
        row["first_funding_at"].date() if pd.notna(row["first_funding_at"]) else None,
        row["last_funding_at"].date() if pd.notna(row["last_funding_at"]) else None,
        row["seed"] if pd.notna(row["seed"]) else None,
        row["venture"] if pd.notna(row["venture"]) else None,
        row["equity_crowdfunding"] if pd.notna(row["equity_crowdfunding"]) else None,
        row["undisclosed"] if pd.notna(row["undisclosed"]) else None,
        row["convertible_note"] if pd.notna(row["convertible_note"]) else None,
        row["debt_financing"] if pd.notna(row["debt_financing"]) else None,
        row["angel"] if pd.notna(row["angel"]) else None,
        row["grant"] if pd.notna(row["grant"]) else None,
        row["private_equity"] if pd.notna(row["private_equity"]) else None,
        row["post_ipo_equity"] if pd.notna(row["post_ipo_equity"]) else None,
        row["post_ipo_debt"] if pd.notna(row["post_ipo_debt"]) else None,
        row["secondary_market"] if pd.notna(row["secondary_market"]) else None,
        row["product_crowdfunding"] if pd.notna(row["product_crowdfunding"]) else None,
        row["round_A"] if pd.notna(row["round_A"]) else None,
        row["round_B"] if pd.notna(row["round_B"]) else None,
        row["round_C"] if pd.notna(row["round_C"]) else None,
        row["round_D"] if pd.notna(row["round_D"]) else None,
        row["round_E"] if pd.notna(row["round_E"]) else None,
        row["round_F"] if pd.notna(row["round_F"]) else None,
        row["round_G"] if pd.notna(row["round_G"]) else None,
        row["round_H"] if pd.notna(row["round_H"]) else None
    ))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Data loaded successfully into PostgreSQL!")