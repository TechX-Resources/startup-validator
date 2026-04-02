-- ============================================
-- Startup Intelligence Query Collection
-- For: Startup Idea Validator Agent
-- ============================================

-- 1. Top funded startups (non-null funding only)
SELECT s.name, f.funding_total_usd
FROM startups s
JOIN funding_profile f ON s.startup_id = f.startup_id
WHERE f.funding_total_usd IS NOT NULL
ORDER BY f.funding_total_usd DESC
LIMIT 10;

-- 2. Startups in the Software market
SELECT s.name, m.market_name
FROM markets m
JOIN startups s ON s.market_id = m.market_id
WHERE m.market_name = 'Software'
LIMIT 10;

-- 3. Startups in USA
SELECT s.name, l.country_code
FROM startups s
JOIN locations l ON s.location_id = l.location_id
WHERE l.country_code = 'USA'
LIMIT 10;

-- 4. Venture-backed startups
SELECT s.name, f.venture
FROM startups s
JOIN funding_profile f ON s.startup_id = f.startup_id
WHERE f.venture IS NOT NULL AND f.venture > 0
ORDER BY f.venture DESC
LIMIT 10;

-- 5. Competitor lookup in E-Commerce
SELECT s.name, m.market_name, f.funding_total_usd
FROM markets m
JOIN startups s ON s.market_id = m.market_id
JOIN funding_profile f ON s.startup_id = f.startup_id
WHERE m.market_name = 'E-Commerce'
AND f.funding_total_usd IS NOT NULL
ORDER BY f.funding_total_usd DESC
LIMIT 10;