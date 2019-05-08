
from ..data_access.buildings import list_buildings as da_list_buildings
from ..data_access.buildings import get_building as da_get_building

from ..errors import ItemNotFound

class Building(object):
    def __init__(self):
        self.record_id = None
        self.name = None
        self.height = None
        self.city = None
        self.country = None

    @classmethod
    def from_db(cls, rowproxy):
        inst = cls()
        inst.record_id = rowproxy.id
        inst.name = rowproxy.name
        inst.height = rowproxy.height
        inst.city = rowproxy.city
        inst.country = rowproxy.country
        return inst

    def as_dict(self):
        return {
            'id': self.record_id,
            'name': self.name,
            'height': self.height,
            'city': self.city,
            'country': self.country
        }

def list_buildings(session):
    db_results = da_list_buildings(session)
    return list(map(Building.from_db, db_results))

def get_building(session, building_id):
    db_result = da_get_building(session, building_id)
    if db_result is None:
        raise ItemNotFound(building_id)
    return Building.from_db(db_result)
