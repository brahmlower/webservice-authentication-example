-- Revert authed_buildings:init from pg

BEGIN;

DROP TABLE accounts;
DROP TABLE accounts_google;
DROP TABLE accounts_standard;
DROP TYPE hash_gen;

COMMIT;
