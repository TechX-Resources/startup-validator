-- ============================================
-- Startup Intelligence Database Schema
-- For: Startup Idea Validator Agent
-- ============================================

-- Drop tables if they already exist
DROP TABLE IF EXISTS funding_profile CASCADE;
DROP TABLE IF EXISTS startups CASCADE;
DROP TABLE IF EXISTS markets CASCADE;
DROP TABLE IF EXISTS locations CASCADE;

-- ============================================
-- Markets Table
-- Stores startup category / market intelligence
-- ============================================
CREATE TABLE markets (
    market_id SERIAL PRIMARY KEY,
    market_name VARCHAR(255),
    category_list TEXT
);

-- ============================================
-- Locations Table
-- Stores startup geographic / ecosystem context
-- ============================================
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    country_code VARCHAR(10),
    state_code VARCHAR(50),
    region VARCHAR(255),
    city VARCHAR(255)
);

-- ============================================
-- Startups Table
-- Stores core startup/company information
-- ============================================
CREATE TABLE startups (
    startup_id SERIAL PRIMARY KEY,
    permalink VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    homepage_url TEXT,
    status VARCHAR(50),
    founded_at DATE,
    founded_month DATE,
    founded_quarter VARCHAR(20),
    founded_year INT,
    market_id INT REFERENCES markets(market_id),
    location_id INT REFERENCES locations(location_id)
);

-- ============================================
-- Funding Profile Table
-- Stores startup financial / funding intelligence
-- ============================================
CREATE TABLE funding_profile (
    funding_id SERIAL PRIMARY KEY,
    startup_id INT UNIQUE REFERENCES startups(startup_id) ON DELETE CASCADE,
    funding_total_usd BIGINT,
    funding_rounds INT,
    first_funding_at DATE,
    last_funding_at DATE,
    seed BIGINT,
    venture BIGINT,
    equity_crowdfunding BIGINT,
    undisclosed BIGINT,
    convertible_note BIGINT,
    debt_financing BIGINT,
    angel BIGINT,
    grant_funding BIGINT,
    private_equity BIGINT,
    post_ipo_equity BIGINT,
    post_ipo_debt BIGINT,
    secondary_market BIGINT,
    product_crowdfunding BIGINT,
    round_A BIGINT,
    round_B BIGINT,
    round_C BIGINT,
    round_D BIGINT,
    round_E BIGINT,
    round_F BIGINT,
    round_G BIGINT,
    round_H BIGINT
);