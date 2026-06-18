-- ============================================================
-- 07_lollov_lol_queues.sql
-- Queue ID to description mapping (from Riot queues.json).
-- Source of truth: LOL_QUEUE_LOV.sql
--                  lol_queues.py (confirms column names in INSERT)
-- ============================================================

CREATE TABLE "lollov".lol_queues
(
    queueid     int,
    "map"       varchar,
    description varchar,
    notes       varchar
);
