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
        self.book_controller.return_book(**request.media)
        response.media = {'message': 'book returned'}

    @join_point
    def on_get_get_all_books(self, request: Request, response: Response):
        books = self.book_controller.get_all()
        response.media = {'library': [{
            'book id': book.book_id,
            'title': book.book_title,
            'author': book.author_name,
            'current owner': book.user_id
        } for book in books]}

    @authenticate
    @join_point
    def on_get_get_user_books(self, request: Request, response: Response):
        user_id = int(request.context.client.user_id)
        books = self.book_controller.get_user_books(user_id)
        response.media = {f'user {request.context.client.user_id} books': [{
            'book id': book.book_id,
            'title': book.book_title,
            'author': book.author_name,
            'current owner': book.user_id
        } for book in books]}

    @join_point
    def on_get_get_free_books(self, request: Request, response: Response):
        books = self.book_controller.get_free_books()
        response.media = {f'user {request.context.client.user_id} books': [{
            'book id': book.book_id,
            'title': book.book_title,
            'author': book.author_name
        } for book in books]}
