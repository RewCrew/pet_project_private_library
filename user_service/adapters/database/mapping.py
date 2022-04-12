from sqlalchemy.orm import registry

from user_service.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.users)
