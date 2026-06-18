-- ============================================================
-- 11_lollov_lol_champions.sql
-- Champion stat table (older, loaded from local dragontail JSON).
-- Used by the CHAMPION_MASTERY view for champion name lookups.
-- Source of truth: champions_lov.py (INSERT and UPDATE queries
--                  confirm all column names)
-- ============================================================

CREATE TABLE "lollov".lol_champions
(
    champion_id              int,
    champion_name            varchar,
    partype                  varchar,
    hp                       real,
    hp_per_level             real,
    mp                       real,
    mp_per_level             real,
    movespeed                real,
    armor                    real,
    armorperlevel            real,
    mr                       real,
    mr_per_level             real,
    attackrange              real,
    hp_regen                 real,
    hp_regen_per_level       real,
    mp_regen                 real,
    mp_regen_per_level       real,
    crit                     real,
    crit_per_level           real,
    attack_damage            real,
    attack_damage_per_level  real,
    attack_speed_per_level   real,
    attack_speed             real,
    patch_no                 varchar
);
