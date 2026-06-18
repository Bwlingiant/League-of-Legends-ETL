-- ============================================================
-- 12_lollov_champions.sql
-- Champion stat table (newer, full ddragon per-champion JSON).
-- Source of truth: champ_lov.py (INSERT query with ON CONFLICT
--                  is fully authoritative for all column names)
-- Notes:
--   - Uses ddragon stat naming conventions (hpperlevel vs
--     hp_per_level used in the older lol_champions table).
--   - tags is a text array (JSON array of role strings).
--   - ON CONFLICT (id) means id must be the PRIMARY KEY.
-- ============================================================

CREATE TABLE "lollov".champions
(
    id                   varchar      PRIMARY KEY,
    key                  varchar,
    name                 varchar,
    title                varchar,
    blurb                text,
    info_attack          int,
    info_defense         int,
    info_magic           int,
    info_difficulty      int,
    tags                 text[],
    partype              varchar,
    hp                   real,
    hpperlevel           real,
    mp                   real,
    mpperlevel           real,
    movespeed            real,
    armor                real,
    armorperlevel        real,
    spellblock           real,
    spellblockperlevel   real,
    attackrange          real,
    hpregen              real,
    hpregenperlevel      real,
    mpregen              real,
    mpregenperlevel      real,
    crit                 real,
    critperlevel         real,
    attackdamage         real,
    attackdamageperlevel real,
    attackspeedperlevel  real,
    attackspeed          real,
    patch_version        varchar
);
