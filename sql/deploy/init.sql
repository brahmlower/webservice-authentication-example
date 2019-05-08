-- Deploy authed_buildings:init to pg

BEGIN;

CREATE USER service_user with encrypted password 'service_user_password';
GRANT ALL PRIVILEGES ON DATABASE buildings_db TO service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO service_user;

-- Base definition of an account. Authentication records reference this object.
CREATE TABLE accounts (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR NOT NULL,
    login_enabled   BOOLEAN NOT NULL DEFAULT TRUE
);

-- Auth records for Google OAuth
CREATE TABLE accounts_google (
    id          SERIAL PRIMARY KEY,
    account_id  INTEGER REFERENCES accounts(id),
    name        VARCHAR NOT NULL,
    email       VARCHAR NOT NULL
);

-- Hash generation type for standard authentication. This just denotes versions of
-- hashing strategies, which makes it useful for tracking credential migrations.
CREATE TYPE hash_gen AS ENUM (
    'gen_0',
    'gen_1'
);

-- Auth records for "Standard" authentication, using a traditional username/password.
CREATE TABLE accounts_standard (
    id          SERIAL PRIMARY KEY,
    account_id  INTEGER REFERENCES accounts(id) UNIQUE,
    username    VARCHAR NOT NULL UNIQUE,
    password    VARCHAR NOT NULL,
    compromised BOOLEAN NOT NULL,
    hash_gen    hash_gen NOT NULL
);

COMMIT;
