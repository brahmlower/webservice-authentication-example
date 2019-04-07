
from ..data_access.buildings import list_buildings as da_list_buildings
from ..data_access.buildings import get_building as da_get_building

def list_buildings(session):
    return da_list_buildings(session)

def get_building(session, building_id):
    return da_get_building(session, building_id)
