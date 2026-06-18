-- ============================================================
-- 03_yrden_lol_ranked_data.sql
-- Ranked queue snapshot per player.
-- Source of truth: ranked_data_table_creation.txt
--                  RANKED_DATA_TABLE_INSERT.txt (confirms column names)
-- Notes:
--   - Original DDL had a typo: "summmoner_id" (triple m).
--     Fixed here to "summoner_id".
--   - person_id FK references yrden.people.
--   - Run 01_yrden_people.sql before this file.
-- ============================================================

CREATE TABLE "yrden".lol_ranked_data
(
    summoner_id      varchar,
    person_id        int,
    puuid            varchar,
    queue_type       varchar,
    league_points    smallint,
    tier             varchar,
    "rank"           varchar,
    wins             smallint,
    losses           smallint,
    hotstreak        boolean,
    ranked_load_date timestamp,

    CONSTRAINT fk_ranked_data_person_id
        FOREIGN KEY (person_id)
        REFERENCES "yrden".people (person_id)
);

CREATE INDEX idx_riot_puuid_ranked
    ON "yrden".lol_ranked_data (puuid);
