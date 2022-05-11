import datetime
from unittest.mock import Mock

import pytest

from classic.messaging import Publisher

from book_service.application import dataclasses, interfaces


@pytest.fixture(scope='function')
def book():
    return dataclasses.Book(
        title='test_title',
        subtitle='test_subtitle',
        authors='test_authors',
        publisher='test_publisher',
        isbn13=123456781234,
        pages=300,
        year=2022,
        rating=5,
        desc='test_desc',
        price=10,
        image='test_image',
        url='test_url',
        isbn10='1234567891',
        book_id=1
    )


@pytest.fixture(scope='function')
def book2():
    return dataclasses.Book(
        title='test_title',
        subtitle='test_subtitle',
        authors='test_authors',
        publisher='test_publisher',
        isbn13=123456781232,
        pages=300,
        year=2022,
        rating=5,
        desc='test_desc',
        price=10,
        image='test_image',
        url='test_url',
        isbn10='1234567891',
        book_id=2
    )


@pytest.fixture(scope='function')
def userbooks():
    return dataclasses.UserBooks(
        book_isbn=123456781234,
        booked_date=datetime.date(2022, 4, 16),
        order_for_days=7,
        prebooked_by_user_id=1,
        finally_booked_by_user_id=None,
        returned=False,
        return_date=datetime.date(2022, 4, 16) + (datetime.timedelta(7)),
        booked_forever=False,
        id=1,
        user_id_history=1
    )


@pytest.fixture(scope='function')
def userbooks_find():
    return dataclasses.UserBooks(
        book_isbn=123456781234,
        booked_date=datetime.date(2022, 4, 16),
        order_for_days=7,
        prebooked_by_user_id=None,
        finally_booked_by_user_id=None,
        returned=False,
        return_date=datetime.date(2022, 4, 16) + (datetime.timedelta(7)),
        booked_forever=False,
        id=1,
        user_id_history=1
    )


@pytest.fixture(scope='function')
def userbooks_return():
    return dataclasses.UserBooks(
        book_isbn=123456781234,
        booked_date=datetime.date(2022, 4, 16),
        order_for_days=7,
        prebooked_by_user_id=None,
        finally_booked_by_user_id=None,
        returned=True,
        return_date=datetime.date.today(),
        booked_forever=False,
        id=1,
        user_id_history=1
    )


@pytest.fixture(scope='function')
def userbooks_buy():
    return dataclasses.UserBooks(
        book_isbn=123456781234,
        booked_date=datetime.date(2022, 4, 16),
        order_for_days=7,
        prebooked_by_user_id=1,
        finally_booked_by_user_id=1,
        returned=False,
        return_date=datetime.date.today(),
        booked_forever=True,
        id=1,
        user_id_history=1
    )


@pytest.fixture(scope='function')
def books_repo(
    book, book2, userbooks, userbooks_return, userbooks_buy, userbooks_find
):
    books_repo = Mock(interfaces.BooksRepo)
    books_repo.add_book = Mock(return_value=book)
    books_repo.get_by_isbn = Mock(return_value=book)
    books_repo.get_or_create = Mock(return_value=book)
    books_repo.get_all = Mock(return_value=[book, book2])
    books_repo.return_book = Mock(return_value=userbooks_return)
    books_repo.buy_book = Mock(return_value=userbooks_buy)
    books_repo.prebook_book = Mock(return_value=userbooks)
    books_repo.get_by_isbn_userbooks = Mock(return_value=userbooks_find)
    books_repo.userbook_create = Mock(return_value=userbooks)

    return books_repo


@pytest.fixture(scope='function')
def book_publisher():
    book_publisher = Mock(Publisher)
    book_publisher.publish = Mock(return_value=None)
    return book_publisher
