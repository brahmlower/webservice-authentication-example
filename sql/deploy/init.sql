-- Deploy authed_buildings:init to pg

BEGIN;

-- Base definition of an account. Authentication records reference this object.
CREATE TABLE accounts (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR NOT NULL
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
