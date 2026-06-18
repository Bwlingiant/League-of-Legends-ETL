-- ============================================================
-- 04_yrden_lol_champ_mastery.sql
-- Champion mastery scores per player.
-- Source of truth: champion mastery table SQL.txt
--                  Get_Champ_Mastery_YRDEN.py (commented-out DDL
--                  block confirms lastplaytime column; the view
--                  CHAMPION_MASTERY also selects LCM.LASTPLAYTIME)
-- Notes:
--   - Original DDL file was missing lastplaytime. Added here.
--   - Logical key: (puuid, championId).
-- ============================================================

CREATE TABLE "yrden".lol_champ_mastery
(
    puuid                         varchar,
    summonerid                    varchar,
    championid                    int,
    championlevel                 int,
    championpoints                int,
    championpointsuntilnextlevel  int,
    championpointssincelastlevel  int,
    lastplaytime                  timestamp,
    chestgranted                  boolean,
    tokensearned                  int
);
