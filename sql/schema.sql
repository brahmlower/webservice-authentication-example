
CREATE TABLE buildings (
    id      serial PRIMARY KEY,
    name    varchar NOT NULL,
    height  integer NOT NULL,
    city    varchar NOT NULL,
    country varchar NOT NULL,
    row_permissions text NOT NULL
);

ALTER TABLE buildings ENABLE ROW LEVEL SECURITY;
ALTER TABLE buildings FORCE ROW LEVEL SECURITY;

CREATE POLICY buildings_policy ON buildings
USING (row_permissions LIKE current_setting('authed_buildings.username'))
WITH CHECK (row_permissions LIKE current_setting('authed_buildings.username'));

-- CREATE A READONLY USER

CREATE USER read_only_user;
ALTER USER read_only_user WITH PASSWORD 'read_only_user';
GRANT CONNECT ON DATABASE "buildings-db" TO read_only_user;
GRANT USAGE ON SCHEMA public TO read_only_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO read_only_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO read_only_user;

-- AUTH RELATED TABLES

CREATE TABLE accounts (
    id      serial PRIMARY KEY,
    name    varchar NOT NULL
);

CREATE TABLE accounts_google (
    id          serial PRIMARY KEY,
    account_id  INTEGER REFERENCES accounts(id),
    name        varchar NOT NULL,
    email       varchar NOT NULL
);

CREATE TYPE hash_gen AS ENUM (
    'gen_0',
    'gen_1'
);

CREATE TABLE accounts_standard (
    id          serial PRIMARY KEY,
    account_id  INTEGER REFERENCES accounts(id) UNIQUE,
    username    varchar NOT NULL UNIQUE,
    password    varchar NOT NULL,
    compromised boolean NOT NULL,
    hash_gen    hash_gen NOT NULL
);

-- 2 FACTOR LATER
