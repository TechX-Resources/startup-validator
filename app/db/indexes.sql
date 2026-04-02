-- ============================================
-- PostgreSQL Indexes for Startup Intelligence DB
-- Purpose: Faster financial and business data retrieval
-- ============================================

-- ============================
-- Startups Table Indexes
-- ============================
CREATE INDEX idx_startups_name ON startups(name);
CREATE INDEX idx_startups_status ON startups(status);
CREATE INDEX idx_startups_founded_year ON startups(founded_year);

-- ============================
-- Markets Table Indexes
-- ============================
CREATE INDEX idx_markets_market_name ON markets(market_name);

-- ============================
-- Locations Table Indexes
-- ============================
CREATE INDEX idx_locations_country_code ON locations(country_code);
CREATE INDEX idx_locations_region ON locations(region);
CREATE INDEX idx_locations_city ON locations(city);

-- ============================
-- Funding Profile Table Indexes
-- ============================
CREATE INDEX idx_funding_total_usd ON funding_profile(funding_total_usd);
CREATE INDEX idx_funding_rounds ON funding_profile(funding_rounds);
CREATE INDEX idx_first_funding_at ON funding_profile(first_funding_at);
CREATE INDEX idx_last_funding_at ON funding_profile(last_funding_at);

-- Funding type indexes for financial retrieval
CREATE INDEX idx_seed ON funding_profile(seed);
CREATE INDEX idx_venture ON funding_profile(venture);
CREATE INDEX idx_angel ON funding_profile(angel);
CREATE INDEX idx_private_equity ON funding_profile(private_equity);
CREATE INDEX idx_grant_funding ON funding_profile(grant_funding);