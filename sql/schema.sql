
CREATE TABLE buildings (
    id      serial PRIMARY KEY,
    name    varchar NOT NULL,
    height  integer NOT NULL,
    city    varchar NOT NULL,
    country varchar NOT NULL
);

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
    'gen_1'
);

CREATE TABLE accounts_standard (
    id          serial PRIMARY KEY,
    account_id  INTEGER REFERENCES accounts(id) UNIQUE,
    username    varchar NOT NULL UNIQUE,
    password    varchar NOT NULL,
    salt        varchar NOT NULL,
    compromised boolean NOT NULL,
    hash_gen    hash_gen
);

-- 2 FACTOR LATER
