from sqlalchemy import text

def buildings_all(engine):
    """ Gets all buildings from the database """
    sql = text("SELECT id, name, height, city, country FROM buildings")
    result = engine.execute(sql)
    return result.fetchall()

def buildings_get(engine, building_id):
    """ Gets a specific building from the database """
    sql = text("SELECT id, name, height, city, country FROM buildings WHERE id = :building_id")
    result = engine.execute(sql, {'building_id': building_id})
    return result.fetchone()

def account_base_create(engine, name):
    sql = text("INSERT INTO accounts(name) VALUES (:name) RETURNING id, name")
    result = engine.execute(sql, {'name': name})
    return result.fetchone()

def account_standalone_create(engine, base_account_id, username, password):
    salt = 'some random salt'
    compromised = False
    hash_gen = 'gen_1'
    sql = text("INSERT INTO accounts_standalone(account_id, username, password, salt, compromised, hash_gen) VALUES(:account_id, :username, :password, :salt, :compromised, :hash_gen) RETURNING *")
    result = engine.execute(sql, {
        'account_id': base_account_id,
        'username': username,
        'password': password,
        'salt': salt,
        'compromised': compromised,
        'hash_gen': hash_gen
    })
    return result.fetchone()

def account_google_create(engine, base_account_id, name, email):
    sql = text("INSERT INTO accounts_google(account_id, name, email) VALUES(:account_id, :name, :email)")
    result = engine.execute(sql, {
        'account_id': base_account_id,
        'name': name,
        'email': email
    })
    return result.fetchone()

def account_get_by_id(engine, account_id):
    """ Get an account by id """
    sql = text("SELECT * FROM accounts WHERE id = :account_id")
    result = engine.execute(sql, {'account_id': account_id})
    return result.fetchone()

def account_login_standalone(engine, username, password):
    # https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Password_Storage_Cheat_Sheet.md
    # TODO: PASSWORD STORAGE MECHANISM OVERHAUL
    """ Get an account ID where the username and password match an entry """
    sql = text("SELECT account_id FROM accounts_standalone WHERE username like :username AND password like :password")
    result = engine.execute(sql, {'username': username, 'password': password})
    return result.fetchone()

def account_login_google(engine, email_address):
    """ This is a wrapper for getting an account by email address """
    sql = text("SELECT account_id FROM accounts_google WHERE email like :email_address")
    result = engine.execute(sql, {'email_address': email_address})
    return result.fetchone()
