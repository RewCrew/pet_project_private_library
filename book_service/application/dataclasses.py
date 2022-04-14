import datetime
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
    isbn10: Optional[str] = None
    # prebooked_by_user_id : Optional[int]=None
    # finally_booked_by_user_id: Optional[int] = None
    book_id: Optional[int] = None


@attr.dataclass
class UserBooks:
    book_isbn: Optional[int] = None
    booked_date: Optional[datetime.date] = None
    order_for_days: Optional[int] = 7
    prebooked_by_user_id: Optional[int] = None
    finally_booked_by_user_id: Optional[int] = None
    returned: Optional[bool] = False
    return_date: Optional[datetime.date] = None
    booked_forever: Optional[bool] = False
    id: Optional[int] = None
    user_id_history:[int]=None
