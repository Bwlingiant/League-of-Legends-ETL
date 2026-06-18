-- ============================================================
-- 05_yrden_lol_challenges.sql
-- Riot challenge progress per player.
-- Source of truth: yrden_challenges.py (STAGE_LOL_CHALLENGES DDL
--                  and INSERT statements are authoritative —
--                  no standalone DDL file exists for this table)
-- Notes:
--   - Logical key: (puuid, challenge_id).
--   - Run 14_lollov_lol_challenges.sql before creating the
--     LEAGUE_CHALLENGES view so the FK join target exists.
-- ============================================================

CREATE TABLE "yrden".lol_challenges
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
