-- Deploy authed_buildings:test_data to pg

BEGIN;

INSERT INTO accounts
(id, name, login_enabled)
VALUES
(0, 'Public', FALSE),
(1, 'Bob Bobberson', TRUE);

INSERT INTO accounts_standard
(id,    account_id, username,   password,   compromised,    hash_gen)
VALUES
(0,     1,          'bob',      'burgers',  FALSE,          'gen_0');

INSERT INTO buildings
(id, name,                              height, city,               country,                owner_id,   is_public)
VALUES
(1,  'Burj Khalifa',                    828,    'Dubai',           'United Arab Emirates',  0,          TRUE),
(2,  'Shanghai Tower',                  632,    'Shanghai',        'China',                 0,          TRUE),
(3,  'Abraj Al-Bait Clock Tower',       601,    'Mecca',           'Saudi Arabia',          0,          TRUE),
(4,  'Ping An Finance Centre',          599,    'Shenzhen',        'China',                 0,          TRUE),
(5,  'Lotte World Tower',               554,    'Seoul',           'South Korea',           0,          TRUE),
(6,  'One World Trade Center',          541,    'New York City',   'United States',         0,          TRUE),
(7,  'Guangzhou CTF Finance Centre',    530,    'Guangzhou',       'China',                 0,          TRUE),
(8,  'Tianjin CTF Finance Centre',      530,    'Tianjin',         'China',                 0,          TRUE),
(9,  'China Zun',                       528,    'Beijing',         'China',                 0,          TRUE),
(10, 'Taipei 101',                      508,    'Taipei',          'Taiwan',                0,          TRUE);

COMMIT;
