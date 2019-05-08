-- Revert authed_buildings:init from pg

BEGIN;

DROP TABLE accounts_standard;
DROP TABLE accounts_google;
DROP TABLE accounts;
DROP TYPE hash_gen;

ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM service_user;
-- REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM service_user;
-- REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM service_user;
-- REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM service_user;
REVOKE ALL PRIVILEGES ON DATABASE buildings_db FROM service_user;
DROP USER service_user;

COMMIT;
