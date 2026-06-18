-- ============================================================
-- 08_lollov_lol_runes.sql
-- Rune ID to name mapping (older, patch-versioned table).
-- Used by the LEAGUE_MATCH_DATA view for rune name lookups.
-- Source of truth: RUNE_LOV_CREATION.txt
--                  LEAGUE MATCH DATA VIEW CREATION.txt (confirms
--                  patch_id column — joined as:
--                  substring(GAME_PATCH,2) = substring(PATCH_ID,2))
-- Notes:
--   - Original DDL was missing patch_id. Added here.
--   - Populated via runes_lov.py (inserts into lollov.runes, the
--     newer table), but this older table is what the view joins.
-- ============================================================

CREATE TABLE "lollov".lol_runes
(
    rune_id   smallint,
    rune_name varchar,
    patch_id  varchar,

    CONSTRAINT unique_rune_id UNIQUE (rune_id, patch_id)
);

CREATE INDEX idx_rune_id
    ON "lollov".lol_runes (rune_id);
