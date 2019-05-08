-- Revert authed_buildings:buildings_table from pg

BEGIN;

DROP POLICY buildings_policy ON buildings;
DROP TABLE buildings;

COMMIT;
