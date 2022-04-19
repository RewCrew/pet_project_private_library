

import pytest
from attr import asdict

from book_service.adapters.database import tables
from book_service.adapters.database.repositories import BooksRepo


@pytest.fixture(scope='function')
def fill_db(session, book, book2, userbooks):
    books_data = [asdict(book), asdict(book2)]
    userbook_take = [asdict(userbooks)]
    session.execute(tables.books.insert(), books_data)
    session.execute(tables.userbooks.insert(), userbook_take)

@pytest.fixture(scope='function')
def books_repo(transaction_context):
    return BooksRepo(context=transaction_context)


def test_get_by_isbn(books_repo, fill_db, book):
    result = books_repo.get_by_isbn(isbn=123456781234)
    assert result == book


def test_get_all(books_repo, fill_db, book, book2):
    result = books_repo.get_all()
    assert result == [book, book2]


def test_prebook_book(books_repo, userbooks, session):
    initial_result = session.execute(tables.userbooks.select()).all()
    assert len(initial_result) == 0
    books_repo.userbook_create(userbooks)
    result = session.execute(tables.userbooks.select()).all()
    assert len(result) == 1


def test_buy_book(fill_db, userbooks_buy, books_repo, session):
    initial_result = session.execute(tables.userbooks.select()).all()
    assert  len(initial_result)==1
    books_repo.buy_book(book_isbn = 123456781234, user_id =1)
    result = session.execute(tables.userbooks.select()).all()
    assert len(result)==1

def test_get_by_isbn_userbooks(books_repo, fill_db, userbooks):
    result = books_repo.get_by_isbn_userbooks(isbn=123456781234)
    assert result == userbooks

