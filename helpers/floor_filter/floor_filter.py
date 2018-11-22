from api.floor.models import Floor
from api.location.models import Location
from api.block.models import Block
from api.office.models import Office


def location_join_floor():
    location_query = Location.query.join(Office).join(Block).join(Floor)
    return location_query


def location_join_block():
    location_query = Location.query.join(Office).join(Block)
    return location_query
