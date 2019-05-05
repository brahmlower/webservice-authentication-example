
INSERT INTO buildings(id, name, height, city, country, row_permissions) VALUES
(1,  'Burj Khalifa',                    828, 'Dubai',           'United Arab Emirates', 'public'),
(2,  'Shanghai Tower',                  632, 'Shanghai',        'China', 'public'),
(3,  'Abraj Al-Bait Clock Tower',       601, 'Mecca',           'Saudi Arabia', 'brahm'),
(4,  'Ping An Finance Centre',          599, 'Shenzhen',        'China', 'public'),
(5,  'Lotte World Tower',               554, 'Seoul',           'South Korea', 'public'),
(6,  'One World Trade Center',          541, 'New York City',   'United States', 'public'),
(7,  'Guangzhou CTF Finance Centre',    530, 'Guangzhou',       'China', 'public'),
(8,  'Tianjin CTF Finance Centre',      530, 'Tianjin',         'China', 'public'),
(9,  'China Zun',                       528, 'Beijing',         'China', 'public'),
(10, 'Taipei 101',                      508, 'Taipei',          'Taiwan', 'public');

INSERT INTO accounts(id, name) VALUES
(0, 'Bob Bobberson');

INSERT INTO accounts_standard(id, account_id, username, password, compromised, hash_gen) VALUES
(0, 0, 'bob', 'burgers', false, 'gen_0');
