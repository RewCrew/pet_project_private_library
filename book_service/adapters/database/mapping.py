from sqlalchemy.orm import registry

from book_service.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.Book, tables.books)
mapper.map_imperatively(dataclasses.UserBooks, tables.userbooks)
