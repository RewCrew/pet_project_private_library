import pytest
from attr import asdict
from book_service.application import services, errors, dataclasses


@pytest.fixture(scope='function')
def book_test(books_repo, book_publisher):
    return services.BookService(books_repo=books_repo, publisher=book_publisher)


test_data_book = {
    'book_id': 1,
    'book_title': 'book',
    'author_name': 'author',
    'user_id': None
}

test_data_book_user = {
    'book_id': 1,
    'book_title': 'book',
    'author_name': 'author',
    'user_id': 1
}

user_id = {'user_id': 1}

book_update = {'author_name': 'updated_author',
               'book_id': 1}

wrong_book_update = {'author_name': 'updated_author',
                     'book_id': 2}


def test_add_book(book_test):
    book_test.add_book(**test_data_book)
    book_test.books_repo.add.assert_called_once()
    book = book_test.get_book(test_data_book['book_id'])
    assert asdict(book) == test_data_book


def test_get_book(book_test):
    book = book_test.get_book(test_data_book['book_id'])
    assert asdict(book) == test_data_book


def test_wrong_book(book_test):
    with pytest.raises(errors.NoBook):
        book_test.get_book(2)


def test_get_all_books(book_test):
    books = book_test.get_all()
    assert type(books) is dataclasses.Book


def test_update_book(book_test):
    book_test.update(**book_update)
    book = book_test.books_repo.get_by_id(test_data_book['book_id'])
    assert book.author_name == book_update['author_name']


def test_wrong_update_book(book_test):
    with pytest.raises(errors.NoBook):
        book_test.update(**wrong_book_update)


def test_take_book(book_test):
    book = book_test.take_book(book_id=1, user_id=1)
    assert asdict(book) == test_data_book_user


def test_return_book(book_test):
    book = book_test.return_book(book_id=1, user_id=1)
    assert asdict(book) == test_data_book
