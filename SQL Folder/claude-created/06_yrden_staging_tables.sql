-- ============================================================
-- 06_yrden_staging_tables.sql
-- Transient ETL staging tables.
-- These are dropped and recreated on every ETL run by the
-- Python scripts. Provided here for reference / initial setup.
-- Source of truth: collect_match_data.py (stage_lol_game_data)
--                  yrden_challenges.py   (stage_lol_challenges)
--                  Get_Champ_Mastery_YRDEN.py (stage_champ_mastery)
-- ============================================================

-- Staging table for new game IDs before full data is pulled
CREATE TABLE "yrden".stage_lol_game_data
(
    puuid   varchar,
    game_id varchar,
    riot_id varchar
);

-- Staging table for challenge data before merge into lol_challenges
CREATE TABLE "yrden".stage_lol_challenges
(
    puuid            varchar,
    challenge_id     integer,
    percentile       real,
    pos              int,
    players_in_level int,
    challenge_level  varchar,
    value            real,
    achieved_time    timestamp
);

-- Staging table for champion mastery before merge into lol_champ_mastery
CREATE TABLE "yrden".stage_champ_mastery
(
    puuid                         varchar,
    championid                    int,
    championlevel                 int,
    championpoints                int,
    championpointsuntilnextlevel  int,
    championpointssincelastlevel  int,
    tokensearned                  int
);
