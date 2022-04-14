from typing import Optional

import attr


@attr.dataclass
class Book:
    title: str
    subtitle: str
    authors: str
    publisher: str
    isbn13: int
    pages: int
    year: int
    rating: int
    desc: str
    price: str
    image: str
    url: str
    # pdf: str
    isbn10: Optional[str]=None
    prebooked_by_user_id : Optional[int]=None
    finally_booked_by_user_id: Optional[int] = None
    book_id: Optional[int] = None
