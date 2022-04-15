import pytest
from unittest.mock import Mock
from book_service.application import interfaces, dataclasses
from evraz.classic.messaging import Publisher


@pytest.fixture(scope='function')
def book():
    return dataclasses.Book(
        book_id=1, book_title='book', author_name='author', user_id=None
    )


@pytest.fixture(scope='function')
def book_taken():
    return dataclasses.Book(
        book_id=1, book_title='book', author_name='author', user_id=1
    )


@pytest.fixture(scope='function')
def books_repo(book, book_taken):
    books_repo = Mock(interfaces.BooksRepo)
    books_repo.get_by_id = Mock(return_value=book)
    books_repo.get_or_create = Mock(return_value=book)
    books_repo.get_all = Mock(return_value=book)
    books_repo.take_book = Mock(return_value=book_taken)
    books_repo.return_book = Mock(return_value=book)

    return books_repo


@pytest.fixture(scope='function')
def book_publisher():
    book_publisher = Mock(Publisher)
    book_publisher.plan = Mock(return_value=None)
    return book_publisher
