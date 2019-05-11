from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import DataError

from ..errors import DatabaseError

def list_buildings(engine):
    """ Gets all buildings from the database """
    sql = text("SELECT id, owner_id, is_public, name, height, city, country FROM buildings ORDER BY id")
    try:
        result = engine.execute(sql)
        return result.fetchall()
    except ProgrammingError as error:
        raise DatabaseError(error)
    except OperationalError as error:
        raise DatabaseError(error)
    except DataError as error:
        raise DatabaseError(error)

def get_building(engine, building_id):
    """ Gets a specific building from the database """
    sql = text("SELECT id, owner_id, is_public, name, height, city, country FROM buildings WHERE id = :building_id")
    try:
        result = engine.execute(sql, {'building_id': building_id})
        return result.fetchone()
    except ProgrammingError as error:
        raise DatabaseError(error)
    except OperationalError as error:
        raise DatabaseError(error)
    except DataError as error:
        raise DatabaseError(error)
