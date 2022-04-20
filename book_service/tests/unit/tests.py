import datetime

import pytest
from attr import asdict
from pydantic import ValidationError

from book_service.application import dataclasses, errors, services


@pytest.fixture(scope='function')
def book_test(books_repo, book_publisher):
    return services.BookService(books_repo=books_repo, publisher=book_publisher)


test_data_book = {
    'title': 'test_title',
    'subtitle': 'test_subtitle',
    'authors': 'test_authors',
    'publisher': 'test_publisher',
    'isbn13': 123456781234,
    'pages': 300,
    'year': 2022,
    'rating': 5,
    'desc': 'test_desc',
    'price': 10,
    'image': 'test_image',
    'url': 'test_url',
    'isbn10': '1234567891',
    'book_id': 1
}

test_data_book2 = {
    'title': 'test_title',
    'subtitle': 'test_subtitle',
    'authors': 'test_authors',
    'publisher': 'test_publisher',
    'isbn13': 123456781232,
    'pages': 300,
    'year': 2022,
    'rating': 5,
    'desc': 'test_desc',
    'price': 10,
    'image': 'test_image',
    'url': 'test_url',
    'isbn10': '1234567891',
    'book_id': 2
}

test_data_userbooks = {
    'book_isbn': 123456781234,
    'booked_date': datetime.date(2022, 4, 16),
    'order_for_days': 7,
    'prebooked_by_user_id': 1,
    'finally_booked_by_user_id': None,
    'returned': False,
    'return_date': datetime.date(2022, 4, 16) + (datetime.timedelta(7)),
    'booked_forever': False,
    'id': 1,
    'user_id_history': 1
}

test_data_userbooks_returned = {
    'book_isbn': 123456781234,
    'booked_date': datetime.date(2022, 4, 16),
    'order_for_days': 7,
    'prebooked_by_user_id': None,
    'finally_booked_by_user_id': None,
    'returned': True,
    'return_date': datetime.date.today(),
    'booked_forever': False,
    'id': 1,
    'user_id_history': 1
}

test_data_book_user = {
    'book_id': 1,
    'book_title': 'book',
    'author_name': 'author',
    'user_id': 1
}

user_id = {'user_id': 1}

book_update = {'author_name': 'updated_author', 'book_id': 1}

wrong_book_update = {'author_name': 'updated_author', 'book_id': 2}


def test_add_book(book_test):
    book = book_test.books_repo.get_or_create(**test_data_book)
    assert asdict(book) == test_data_book


def test_get_book(book_test):
    book = book_test.get_book(test_data_book['isbn13'])
    assert asdict(book) == test_data_book


def test_wrong_book(book_test):
    with pytest.raises(errors.ErrorBook):
        book_test.get_book(2)


def test_get_all_books(book_test):
    books = book_test.get_all()
    assert [asdict(books[0]),
            asdict(books[1])] == [test_data_book, test_data_book2]


def test_prebook_book(book_test):
    prebook = book_test.prebook_book(book_isbn=123456781234, user_id=1)
    print(asdict(prebook))
    assert asdict(prebook) == test_data_userbooks


def test_return_book(book_test):
    book = book_test.return_book(book_isbn=123456781234, user_id=1)

    assert book == 'book returned'


def test_wrong_prebook_book(book_test):
    book_test.books_repo.get_by_isbn.return_value = None
    with pytest.raises(errors.ErrorBook):
        book_test.prebook_book(book_isbn=123456781234, user_id=1)


def test_prebook_book_wrong_args(book_test):
    with pytest.raises(ValidationError):
        book_test.prebook_book(user_id=2)


def test_return_book_wrong_args(book_test):
    with pytest.raises(ValidationError):
        book_test.return_book(user_id=2)


def test_get_book_wrong_args(book_test):
    with pytest.raises(ValidationError):
        book_test.get_book(user_id=2)


def test_add_book_wrong_args(book_test):
    with pytest.raises(ValidationError):
        book_test.add_book(user_id=1)


if __name__ == '__main__':
    pytest.main()