-- ============================================================
-- 13_lollov_champions_info.sql
-- Minimal champion metadata (no stats).
-- Source of truth: champ_base_lov.py (INSERT query with ON
--                  CONFLICT is fully authoritative)
-- ============================================================

CREATE TABLE "lollov".champions_info
(
    id    varchar PRIMARY KEY,
    key   varchar,
    name  varchar,
    title varchar,
    blurb text
);
