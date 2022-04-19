from book_service.composites.app_api import Application as app


def get_books(params: list):
    app.books.get_books_from_api(params=params)

