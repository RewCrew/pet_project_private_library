import falcon
import pytest

from book_service.application import errors


def test_post_prebook_book(books_service, client):
    books_service.prebook_book.return_value = None

    expected = {'message': 'book taken by you'}

    result = client.simulate_post(
        '/api/books/prebook_book',
        content_type=falcon.MEDIA_JSON,
        json={'book_isbn': 9781449344160}
    )

    assert result.status_code == 200
    assert result.json == expected


def test_post_prebook_book_error(books_service, client):
    books_service.prebook_book.side_effect = errors.ErrorBook(
        message="not valid ID of book"
    )

    expected = [
        {
            'ctx': {},
            'msg': 'not valid ID of book',
            'type': 'books.trouble'
        }
    ]

    result = client.simulate_post(
        '/api/books/prebook_book',
        content_type=falcon.MEDIA_JSON,
        json={'book_isbn': 9781449344160}
    )

    assert result.status_code == 400
    assert result.json == expected


def test_get_all_books(books_service, client):
    books_service.get_all.return_value = {}
    expected = {'library': []}
    result = client.simulate_get(
        '/api/books/get_all_books', content_type=falcon.MEDIA_JSON
    )
    assert result.status_code == 200
    assert result.json == expected


def test_get_book(books_service, client, book):
    books_service.get_all.return_value = [book]
    expected = {
        'library': [
            {
                'book id': 1,
                'title': 'test_title',
                'authors': 'test_authors',
                'subtitle': 'test_subtitle',
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
            }
        ]
    }

    result = client.simulate_get(
        '/api/books/get_all_books',
        content_type=falcon.MEDIA_JSON,
        json={'isbn': 123456781234}
    )

    assert result.status_code == 200
    assert result.json == expected


def test_get_user_books(books_service, client, userbooks):
    books_service.get_user_books.return_value = [userbooks]

    expected = {'user 1 active books': [{'book isbn': 123456781234}]}

    result = client.simulate_get(
        '/api/books/get_user_books',
        content_type=falcon.MEDIA_JSON,
        json={'user_id': 1}
    )

    assert result.status_code == 200
    assert result.json == expected


def test_post_buy_book(books_service, client, userbooks_buy):
    books_service.buy_book.return_value = None

    expected = {'message': 'you finally bought this book'}

    result = client.simulate_post(
        '/api/books/buy_book',
        content_type=falcon.MEDIA_JSON,
        json={
            'user_id': 1,
            'book_isbn': 123456781234
        }
    )
    assert result.status_code == 200
    assert result.json == expected


def test_get_history_books(books_service, client, userbooks_find):
    books_service.get_history_user_books.return_value = [userbooks_find]

    expected = {
        'user 1 took and returned next books': [{
            'book isbn': 123456781234
        }]
    }

    result = client.simulate_get(
        '/api/books/get_history_books', content_type=falcon.MEDIA_JSON
    )

    assert result.status_code == 200
    assert result.json == expected


if __name__ == '__main__':
    pytest.main()