-- ============================================================
-- 16_views.sql
-- All views. Run after all table scripts (01-15).
-- Source of truth: LEAGUE MATCH DATA VIEW CREATION.txt
--                  LEAGUE_CHALLENGES_VIEW.txt
--                  REFRESH CHAMPION MASTERY VIEW.txt
-- ============================================================


-- ------------------------------------------------------------
-- View: yrden.league_match_data
-- Joins game data with player info, summoner spells, queue
-- descriptions, and rune names (patch-matched).
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW "yrden".league_match_data AS
SELECT
    lgd.riot_puuid,
    yp.person_id,
    lgd.riot_id,
    lgd.game_patch,
    lgd.game_id,
    lgd.game_mode,
    lgd.queue_id,
    lqv.description,
    lgd.champion_name,
    lgd.champion_id,
    lgd.lane,
    CASE
        WHEN lgd.teamid = 100 THEN 'Blue'
        WHEN lgd.teamid = 200 THEN 'Red'
        ELSE NULL
    END AS map_side,
    lgd.win,
    lgd.kills,
    lgd.deaths,
    lgd.assists,
    CASE
        WHEN lgd.deaths = 0 THEN (lgd.kills + lgd.assists)
        ELSE (lgd.kills + lgd.assists) / lgd.deaths
    END AS kda,
    lgd.double_kills,
    lgd.triple_kills,
    lgd.quadra_kills,
    lgd.penta_kills,
    lgd.gold_earned,
    lgd.champion_damage,
    lgd.objective_damage,
    lgd.damage_healed,
    lgd.vision_score,
    lgd.minions_killed,
    lgd.neutral_monsters_killed,
    lgd.control_wards_purchased,
    lgd.keystone_rune_code,
    ksv.rune_name  AS keystone_rune_name,
    lgd.keystone_rune_var1,
    lgd.keystone_rune_var2,
    lgd.keystone_rune_var3,
    lgd.primary_rune_code1,
    prv1.rune_name AS primary_rune1_name,
    lgd.primary_rune1_var1,
    lgd.primary_rune1_var2,
    lgd.primary_rune1_var3,
    lgd.primary_rune_code2,
    prv2.rune_name AS primary_rune2_name,
    lgd.primary_rune2_var1,
    lgd.primary_rune2_var2,
    lgd.primary_rune2_var3,
    lgd.primary_rune_code3,
    prv3.rune_name AS primary_rune3_name,
    lgd.primary_rune3_var1,
    lgd.primary_rune3_var2,
    lgd.primary_rune3_var3,
    lgd.secondary_rune_code1,
    srv1.rune_name AS secondary_rune1_name,
    lgd.secondary_rune1_var1,
    lgd.secondary_rune1_var2,
    lgd.secondary_rune1_var3,
    lgd.secondary_rune_code2,
    srv2.rune_name AS secondary_rune2_name,
    lgd.secondary_rune2_var1,
    lgd.secondary_rune2_var2,
    lgd.secondary_rune2_var3,
    lgd.largest_critical_strike,
    lgd.nexus_kills,
    lgd.summoner1_casts,
    lgd.summoner1_id,
    lsv1.spell_name AS summonerspell_1,
    lgd.summoner2_casts,
    lgd.summoner2_id,
    lsv2.spell_name AS summonerspell_2,
    lgd.game_duration,
    lgd.wards_killed,
    lgd.wards_placed
FROM "yrden".lol_game_data lgd
INNER JOIN "yrden".people yp
    ON lgd.riot_puuid = yp.riot_puuid
    AND lgd.riot_id   = yp.riot_id
LEFT JOIN "lollov".summoner_spells lsv1
    ON lgd.summoner1_id = lsv1.spell_id
LEFT JOIN "lollov".summoner_spells lsv2
    ON lgd.summoner2_id = lsv2.spell_id
LEFT JOIN "lollov".lol_queues lqv
    ON lgd.queue_id = lqv.queueid
LEFT JOIN "lollov".lol_runes ksv
    ON lgd.keystone_rune_code = ksv.rune_id
    AND substring(lgd.game_patch, 2) = substring(ksv.patch_id, 2)
LEFT JOIN "lollov".lol_runes prv1
    ON lgd.primary_rune_code1 = prv1.rune_id
    AND substring(lgd.game_patch, 2) = substring(prv1.patch_id, 2)
LEFT JOIN "lollov".lol_runes prv2
    ON lgd.primary_rune_code2 = prv2.rune_id
    AND substring(lgd.game_patch, 2) = substring(prv2.patch_id, 2)
LEFT JOIN "lollov".lol_runes prv3
    ON lgd.primary_rune_code3 = prv3.rune_id
    AND substring(lgd.game_patch, 2) = substring(prv3.patch_id, 2)
LEFT JOIN "lollov".lol_runes srv1
    ON lgd.secondary_rune_code1 = srv1.rune_id
    AND substring(lgd.game_patch, 2) = substring(srv1.patch_id, 2)
LEFT JOIN "lollov".lol_runes srv2
    ON lgd.secondary_rune_code2 = srv2.rune_id
    AND substring(lgd.game_patch, 2) = substring(srv2.patch_id, 2)
;


-- ------------------------------------------------------------
-- View: yrden.league_challenges
-- Joins player challenge progress with challenge definitions,
-- calculates points needed to reach the next tier.
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW "yrden".league_challenges AS
SELECT
    yp.riot_puuid,
    yp.riot_id,
    lct.challenge_id,
    lcv.name                                          AS challenge_name,
    lct.value,
    CASE
        WHEN lct.value < lcv.iron        THEN lcv.iron        - lct.value
        WHEN lct.value < lcv.bronze      THEN lcv.bronze      - lct.value
        WHEN lct.value < lcv.silver      THEN lcv.silver      - lct.value
        WHEN lct.value < lcv.gold        THEN lcv.gold        - lct.value
        WHEN lct.value < lcv.platinum    THEN lcv.platinum    - lct.value
        WHEN lct.value < lcv.diamond     THEN lcv.diamond     - lct.value
        WHEN lct.value < lcv.master      THEN lcv.master      - lct.value
        WHEN lct.value < lcv.grandmaster THEN lcv.grandmaster - lct.value
        WHEN lct.value < lcv.challenger  THEN lcv.challenger  - lct.value
        ELSE 0
    END AS points_needed,
    lct.challenge_level,
    lct.achieved_time,
    lct.percentile,
    lcv.tier,
    lcv.shortdescription,
    lcv.iron,
    lcv.bronze,
    lcv.silver,
    lcv.gold,
    lcv.platinum,
    lcv.diamond,
    lcv.master,
    lcv.grandmaster,
    lcv.challenger
FROM "yrden".lol_challenges lct
LEFT JOIN "lollov".lol_challenges lcv
    ON lct.challenge_id = lcv.challenge_id
LEFT JOIN "yrden".people yp
    ON lct.puuid = yp.riot_puuid
;


-- ------------------------------------------------------------
-- View: yrden.champion_mastery
-- Joins champion mastery data with player info and champion
-- name lookup from lollov.lol_champions.
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW "yrden".champion_mastery AS
SELECT
    lcm.puuid,
    yp.riot_id,
    lcm.championid,
    lcv.champion_name,
    lcm.championlevel,
    lcm.championpoints,
    lcm.championpointsuntilnextlevel,
    lcm.championpointssincelastlevel,
    lcm.chestgranted,
    lcm.lastplaytime,
    lcm.tokensearned
FROM "yrden".lol_champ_mastery lcm
LEFT JOIN "yrden".people yp
    ON lcm.puuid = yp.riot_puuid
LEFT JOIN "lollov".lol_champions lcv
    ON lcm.championid = lcv.champion_id
;
