from sqlalchemy import text

def list_buildings(engine):
    """ Gets all buildings from the database """
    sql = text("SELECT id, name, height, city, country FROM buildings")
    result = engine.execute(sql)
    return result.fetchall()

def get_building(engine, building_id):
    """ Gets a specific building from the database """
    sql = text("SELECT id, name, height, city, country FROM buildings WHERE id = :building_id")
    result = engine.execute(sql, {'building_id': building_id})
    return result.fetchone()
