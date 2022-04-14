from book_service.application import services
from evraz.classic.components import component

from .join_points import join_point
from falcon import Request, Response

from evraz.classic.http_auth import (
    authenticate,
    authenticator_needed)


@authenticator_needed
@component
class BooksController:
    book_controller: services.BookService

    @join_point
    def on_post_add_book(self, request: Request, response: Response):
        self.book_controller.add_book(**request.media)
        response.media = {'message': 'book added'}

    #
    @join_point
    def on_post_update(self, request: Request, response: Response):
        self.book_controller.update(**request.media)
        response.media = {'message': 'book updated'}

    @join_point
    def on_post_delete(self, request: Request, response: Response):
        self.book_controller.delete_book(**request.media)
        response.media = {'message': 'book deleted from library'}

    @authenticate
    @join_point
    def on_post_take_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id

        self.book_controller.take_book(**request.media)

        response.media = {'message': 'book taken by you'}

    @authenticate
    @join_point
    def on_post_return_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id
        message = self.book_controller.return_book(**request.media)
        response.media = {'message': message}

    @join_point
    def on_get_get_all_books(self, request: Request, response: Response):
        books = self.book_controller.get_all()
        response.media = {'library': [{
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
            'prebooked_by_user_id': book.prebooked_by_user_id,
            'finally_booked_by_user_id': book.finally_booked_by_user_id
        } for book in books]}

    @join_point
    def on_get_get_book(self, request: Request, response: Response):
        isbn=request.get_param('isbn')
        book = self.book_controller.get_book(int(isbn))
        response.media = {'library': {
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
            'prebooked_by_user_id': book.prebooked_by_user_id,
            'finally_booked_by_user_id': book.finally_booked_by_user_id
        } }


    @authenticate
    @join_point
    def on_get_get_user_books(self, request: Request, response: Response):
        user_id = int(request.context.client.user_id)
        books = self.book_controller.get_user_books(user_id)
        response.media = {f'user {request.context.client.user_id} books': [{
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
        } for book in books]}


    @authenticate
    @join_point
    def on_post_prebook_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id
        self.book_controller.prebook_book(**request.media)

    @authenticate
    @join_point
    def on_post_buy_book(self, request: Request, response: Response):
        request.media['user_id'] = request.context.client.user_id
        self.book_controller.buy_book(**request.media)

