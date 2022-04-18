import falcon
from pydantic import ValidationError
from book_service.application import errors


def test_post_prebook_book(books_service, client):
    books_service.prebook_book.return_value = None

    expected = {'message': 'book taken by you'}

    result = client.simulate_post('/api/books/prebook_book',
                                  content_type = falcon.MEDIA_JSON,
                                  json = {'book_isbn':9781449344160})

    assert result.status_code == 200
    assert result.json == expected


def test_post_prebook_book_error(books_service, client):
    books_service.prebook_book.side_effect = errors.ErrorBook(message="not valid ID of book")

    expected = [{'ctx': {}, 'msg': 'not valid ID of book', 'type': 'books.trouble'}]

    result = client.simulate_post('/api/books/prebook_book',
                                  content_type = falcon.MEDIA_JSON,
                                  json = {'book_isbn':9781449344160})

    assert result.status_code == 400
    assert result.json == expected