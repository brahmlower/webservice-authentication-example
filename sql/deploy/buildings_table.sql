-- Deploy authed_buildings:buildings_table to pg

BEGIN;

CREATE TABLE buildings (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR NOT NULL,
    height      INTEGER NOT NULL,
    city        VARCHAR NOT NULL,
    country     VARCHAR NOT NULL,
    owner_id    INTEGER REFERENCES accounts(id) NOT NULL,
    is_public   BOOLEAN NOT NULL
);

-- Enable row seciruty on the buildings table
ALTER TABLE buildings ENABLE ROW LEVEL SECURITY;
ALTER TABLE buildings FORCE ROW LEVEL SECURITY;

-- Use the users ID to determine what records they have access to. Public
-- records can be viewed by anyone. A user currently can only update
-- records they own (there's no concept of group permissions yet). Public
-- records are denoted by a NULL owner_id.
CREATE POLICY buildings_policy ON buildings
USING ( owner_id = current_setting('authed_buildings.user_id')::INTEGER
    OR  is_public = TRUE
    )
WITH CHECK (
    owner_id = current_setting('authed_buildings.user_id')::INTEGER
    );

COMMIT;
