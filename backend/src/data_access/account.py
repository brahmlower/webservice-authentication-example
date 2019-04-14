from sqlalchemy import text

# Base account interaction -----------------------------------------------------

def account_base_create(engine, name):
    sql = text("INSERT INTO accounts(name) VALUES (:name) RETURNING id, name")
    result = engine.execute(sql, {'name': name})
    return result.fetchone()

def account_base_get_by_id(engine, record_id):
    """ Get an account by id """
    sql = text("SELECT * FROM accounts WHERE id = :record_id")
    result = engine.execute(sql, {'record_id': record_id})
    return result.fetchone()

# Standard account interaction -------------------------------------------------

def account_standard_create(engine, base_account_id, username, password):
    compromised = False
    hash_gen = 'gen_1'
    sql = text("INSERT INTO accounts_standard(account_id, username, password, compromised, hash_gen) VALUES(:account_id, :username, :password, :compromised, :hash_gen) RETURNING *")
    result = engine.execute(sql, {
        'account_id': base_account_id,
        'username': username,
        'password': password,
        'compromised': compromised,
        'hash_gen': hash_gen
    })
    return result.fetchone()

def account_standard_get_by_username(engine, username):
    sql = text("SELECT * FROM accounts_standard WHERE username like :username")
    result = engine.execute(sql, {'username': username})
    return result.fetchone()

def account_standard_update_auth_gen(engine, record_id, password, hash_gen):
    sql = text("UPDATE accounts_standard SET password = :password, hash_gen = :hash_gen WHERE id = :record_id")
    result = engine.execute(sql, {
        'record_id': record_id,
        'password': password,
        'hash_gen': hash_gen
    })
    return result

def account_standard_update_password(engine, record_id, password, hash_gen):
    sql = text("UPDATE accounts_standard SET password = :password, hash_gen = :hash_gen WHERE id = :record_id")
    result = engine.execute(sql, {
        'record_id': record_id,
        'password': password,
        'hash_gen': hash_gen
    })
    return result

# Google account interaction ---------------------------------------------------

def account_google_create(engine, base_account_id, name, email):
    sql = text("INSERT INTO accounts_google(account_id, name, email) VALUES(:account_id, :name, :email)")
    result = engine.execute(sql, {
        'account_id': base_account_id,
        'name': name,
        'email': email
    })
    return result.fetchone()

def account_google_get_by_email(engine, email_address):
    """ This is a wrapper for getting an account by email address """
    sql = text("SELECT account_id FROM accounts_google WHERE email like :email_address")
    result = engine.execute(sql, {'email_address': email_address})
    return result.fetchone()
