-- ============================================================
-- 01_yrden_people.sql
-- Core player registry table.
-- Source of truth: yrden_people table creation.txt
--                  yrden_sql_queries.py (confirms YRDEN_FLAG,
--                  summoner_name, riot_key columns)
--                  add_new_people.py / update_people.py
-- ============================================================

CREATE TABLE "yrden".people
(
    person_id     serial       PRIMARY KEY,
    riot_puuid    varchar,
    riot_id       varchar,
    riot_key      varchar,
    summoner_id   varchar,
    summoner_name varchar,
    name          varchar,
    "YRDEN_FLAG"  boolean
);
