-- Deploy authed_buildings:test_data to pg

BEGIN;

INSERT INTO buildings
(id, name,                              height, city,               country,                owner_id)
VALUES
(1,  'Burj Khalifa',                    828,    'Dubai',           'United Arab Emirates',  NULL),
(2,  'Shanghai Tower',                  632,    'Shanghai',        'China',                 NULL),
(3,  'Abraj Al-Bait Clock Tower',       601,    'Mecca',           'Saudi Arabia',          NULL),
(4,  'Ping An Finance Centre',          599,    'Shenzhen',        'China',                 NULL),
(5,  'Lotte World Tower',               554,    'Seoul',           'South Korea',           NULL),
(6,  'One World Trade Center',          541,    'New York City',   'United States',         NULL),
(7,  'Guangzhou CTF Finance Centre',    530,    'Guangzhou',       'China',                 NULL),
(8,  'Tianjin CTF Finance Centre',      530,    'Tianjin',         'China',                 NULL),
(9,  'China Zun',                       528,    'Beijing',         'China',                 NULL),
(10, 'Taipei 101',                      508,    'Taipei',          'Taiwan',                NULL);

INSERT INTO accounts
(id, name)
VALUES
(0, 'Bob Bobberson');

INSERT INTO accounts_standard
(id,    account_id, username,   password,   compromised,    hash_gen)
VALUES
(0,     0,          'bob',      'burgers',  FALSE,          'gen_0');

COMMIT;
