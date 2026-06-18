-- ============================================================
-- 10_lollov_summoner_spells.sql
-- Summoner spell ID to name mapping.
-- Source of truth: SummonerSpellLOV.py (CREATE TABLE and INSERT
--                  are the authoritative source for this table)
-- Notes:
--   - The LEAGUE_MATCH_DATA view references this as
--     "lollov".LOL_SUMMONER_SPELLS — same table, uppercase alias.
-- ============================================================

CREATE TABLE "lollov".summoner_spells
(
    spell_name varchar,
    spell_id   int,
    modes      varchar
);
