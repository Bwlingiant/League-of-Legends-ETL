-- ============================================================
-- 14_lollov_lol_challenges.sql
-- Challenge definitions with tier threshold values and
-- localized name/description text.
-- Source of truth: challenges_lov.py (INSERT is dynamically
--                  constructed from Riot API response)
--                  CHALLENGES VIEW CREATION.txt (confirms column
--                  names: name, shortdescription, tier, iron
--                  through challenger)
--                  LEAGUE_CHALLENGES_VIEW.txt (same confirmation)
-- Notes:
--   - Column names match Riot API localizedNames['en_US'] keys
--     (name, description, shortDescription) and thresholds keys
--     (IRON, BRONZE, SILVER, GOLD, PLATINUM, DIAMOND, MASTER,
--      GRANDMASTER, CHALLENGER) — lowercased for PostgreSQL.
-- ============================================================

CREATE TABLE "lollov".lol_challenges
(
    challenge_id     int PRIMARY KEY,
    name             varchar,
    description      varchar,
    shortdescription varchar,
    tier             varchar,
    iron             real,
    bronze           real,
    silver           real,
    gold             real,
    platinum         real,
    diamond          real,
    master           real,
    grandmaster      real,
    challenger       real
);
