-- ============================================================
-- 09_lollov_runes.sql
-- Rune definitions — newer table with category and slot info.
-- Source of truth: runes_lov.py (INSERT query is authoritative)
-- ============================================================

CREATE TABLE "lollov".runes
(
    rune_name varchar,
    rune_id   int,
    rune_key  varchar,
    category  varchar,
    rune_slot int
);
