from falcon import Request, Response

from evraz.classic.components import component
from evraz.classic.http_auth import authenticate, authenticator_needed

from book_service.application import services

from .join_points import join_point


@authenticator_needed
@component
class Books:
    books: services.BookService

    @join_point
    def on_post_add_book(self, request: Request, response: Response):
        self.books.add_book(**request.media)
        response.media = {'message': 'book added'}

    @authenticate
    @join_point
    def on_post_take_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id
        self.books.take_book(**request.media)
        response.media = {'message': 'book taken by you'}

    @authenticate
    @join_point
    def on_post_return_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id
        message = self.books.return_book(**request.media)
        response.media = {'message': message}

    @join_point
    def on_get_get_all_books(self, request: Request, response: Response):
        books = self.books.get_all()
        response.media = {
            'library': [
                {
                    'book id': book.book_id,
                    'title': book.title,
                    'authors': book.authors,
                    'subtitle': book.subtitle,
                    'publisher': book.publisher,
                    'isbn13': book.isbn13,
                    'pages': book.pages,
                    'year': book.year,
                    'rating': book.rating,
                    'desc': book.desc,
                    'price': book.price,
                    'image': book.image,
                    'url': book.url,
                    'isbn10': book.isbn10,
                } for book in books
            ]
        }

    @join_point
    def on_get_get_book(self, request: Request, response: Response):
        isbn = request.get_param('isbn')
        book = self.books.get_book(int(isbn))
        response.media = {
            'library': {
                'book id': book.book_id,
                'title': book.title,
                'authors': book.authors,
                'subtitle': book.subtitle,
                'publisher': book.publisher,
                'isbn13': book.isbn13,
                'pages': book.pages,
                'year': book.year,
                'rating': book.rating,
                'desc': book.desc,
                'price': book.price,
                'image': book.image,
                'url': book.url,
                'isbn10': book.isbn10,
            }
        }

    @authenticate
    @join_point
    def on_get_get_user_books(self, request: Request, response: Response):
        user_id = int(request.context.client.user_id)
        books = self.books.get_user_books(user_id)
        response.media = {
            f'user {request.context.client.user_id} active books': [
                {
                    'book isbn': book.book_isbn
                } for book in books
            ]
        }

    @authenticate
    @join_point
    def on_post_prebook_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id
        self.books.prebook_book(**request.media)

    @authenticate
    @join_point
    def on_post_buy_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id
        self.books.buy_book(**request.media)

    @authenticate
    @join_point
    def on_get_get_history_books(self, request: Request, response: Response):
        user_id = int(request.context.client.user_id)
        books = self.books.get_history_user_books(user_id)
        response.media = {
            f'user {request.context.client.user_id} took and returned next books': [
                {
                    'book isbn': book.book_isbn
                } for book in books
            ]
        }

    @join_point
    def on_get_show_filtered_books(self, request: Request, response: Response):
        books = self.books.filter_books(request.params)

        response.media = [
            {
                'book id': book.book_id,
                'title': book.title,
                'authors': book.authors,
                'subtitle': book.subtitle,
                'publisher': book.publisher,
                'isbn13': book.isbn13,
                'pages': book.pages,
                'year': book.year,
                'rating': book.rating,
                'desc': book.desc,
                'price': book.price,
                'image': book.image,
                'url': book.url,
                'isbn10': book.isbn10,
            } for book in books
        ]
