-- ============================================================
-- master_build.sql
-- Run all schema creation scripts in dependency order.
-- Usage (psql):
--   psql -U postgres -d test -f master_build.sql
-- ============================================================

\echo '--- 00: Creating schemas ---'
\i '00_create_schemas.sql'

\echo '--- 01: yrden.people ---'
\i '01_yrden_people.sql'

\echo '--- 02: yrden.lol_game_data ---'
\i '02_yrden_lol_game_data.sql'

\echo '--- 03: yrden.lol_ranked_data ---'
\i '03_yrden_lol_ranked_data.sql'

\echo '--- 04: yrden.lol_champ_mastery ---'
\i '04_yrden_lol_champ_mastery.sql'

\echo '--- 05: yrden.lol_challenges ---'
\i '05_yrden_lol_challenges.sql'

\echo '--- 06: yrden staging tables ---'
\i '06_yrden_staging_tables.sql'

\echo '--- 07: lollov.lol_queues ---'
\i '07_lollov_lol_queues.sql'

\echo '--- 08: lollov.lol_runes ---'
\i '08_lollov_lol_runes.sql'

\echo '--- 09: lollov.runes ---'
\i '09_lollov_runes.sql'

\echo '--- 10: lollov.summoner_spells ---'
\i '10_lollov_summoner_spells.sql'

\echo '--- 11: lollov.lol_champions ---'
\i '11_lollov_lol_champions.sql'

\echo '--- 12: lollov.champions ---'
\i '12_lollov_champions.sql'

\echo '--- 13: lollov.champions_info ---'
\i '13_lollov_champions_info.sql'

\echo '--- 14: lollov.lol_challenges ---'
\i '14_lollov_lol_challenges.sql'

\echo '--- 15: lol.esports_data ---'
\i '15_lol_esports_data.sql'

\echo '--- 16: Views ---'
\i '16_views.sql'

\echo '--- Build complete ---'
