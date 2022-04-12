from typing import Optional
import requests
import json
from book_service.application import errors
from pydantic import validate_arguments

from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component

from . import interfaces
from .dataclasses import Book
from evraz.classic.messaging import Publisher, Message

join_points = PointCut()
join_point = join_points.join_point


class BookInfo(DTO):
    title: str
    subtitle: str
    authors: str
    publisher: str
    isbn13: int
    pages: int
    year: int
    rating: int
    desc: str
    price: str
    image: str
    url: str
    tag: str
    isbn10: Optional[str] = None
    prebooked_by_user_id: Optional[int] = None
    finally_booked_by_user_id: Optional[int] = None
    book_id: Optional[int] = None


class BookInfoUpdate(DTO):
    book_title: Optional[str] = None
    author_name: Optional[str] = None
    book_id: Optional[int] = None


@component
class BookService:
    books_repo: interfaces.BooksRepo
    publisher: Publisher

    @join_point
    # @validate_with_dto
    @validate_arguments
    # def add_book(self, book_info: BookInfo):
    def add_book(self, data: dict):
        book_info = BookInfo(**data)
        new_book = book_info.create_obj(Book)
        book = self.books_repo.get_or_create(new_book)
        # self.publisher.plan(Message("Exchange", {"action": "create",
        #                                          "api": "Book",
        #                                          "api_id": book.book_id}))
        self.books_repo.add(book)

    @join_point
    @validate_with_dto
    def update(self, book_info: BookInfoUpdate):
        book = self.get_book(book_info.book_id)
        book_info.populate_obj(book)
        self.publisher.plan(Message("Exchange", {"action": "update",
                                                 "api": "Book",
                                                 "api_id": book_info.book_id}))

    @join_point
    @validate_arguments
    def delete_book(self, book_id: int):
        self.books_repo.delete(book_id)
        self.publisher.plan(Message("Exchange", {"action": "delete",
                                                 "api": "Book",
                                                 "api_id": book_id}))

    @join_point
    @validate_arguments
    def take_book(self, book_id: int, user_id: int):
        book = self.books_repo.take_book(book_id, user_id)
        self.publisher.plan(Message("Exchange", {"action": "take book",
                                                 "api": "Book",
                                                 "api_id": book_id}))
        self.publisher.plan(Message("Exchange", {"action": "take book",
                                                 "api": "User",
                                                 "api_id": user_id}))
        return book

    @join_point
    @validate_arguments
    def return_book(self, book_id: int, user_id: int):
        book = self.books_repo.return_book(book_id, user_id)
        self.publisher.plan(Message("Exchange", {"action": "return book",
                                                 "api": "Book",
                                                 "api_id": book_id}))
        self.publisher.plan(Message("Exchange", {"action": "return book",
                                                 "api": "User",
                                                 "api_id": user_id}))
        return book

    @join_point
    def get_all(self):
        books = self.books_repo.get_all()
        return books

    @join_point
    @validate_arguments
    def get_user_books(self, user_id: int):
        books = self.books_repo.get_user_books(user_id)
        return books

    @join_point
    def get_free_books(self):
        books = self.books_repo.get_free_books()
        return books

    @join_point
    def get_book(self, book_id: int):
        book = self.books_repo.get_by_id(book_id)
        if book is None or book_id != book.book_id:
            raise errors.NoBook(message="No book exist")
        else:
            return book

    @join_point
    def get_books_from_api(self, params:list):
        books = []
        for param in params:
            for i in range(1,6):
                response = requests.get(f"https://api.itbook.store/1.0/search/{param}/{i}")
                result = response.content.decode("utf8")
                result = json.loads(result)
                if not result["books"]:
                    break
                query = result["books"]
                # PUBLISHER Send message to queue

                # CONSUMER --> GET DETAILS --> SAVE TO REPO
                for book in query:
                    response = requests.get(f"https://api.itbook.store/1.0/books/{book['isbn13']}")
                    result = response.content.decode("utf-8")
                    result = json.loads(result)
                    result['tag'] = param
                    # print(result['isbn10'], type(result['isbn10']))
                    books.append(result)
                    # book_info = BookInfo(**result)
                    # print(book_info)
                    self.publisher.publish(Message("Exchange", {'data': result}))

                # GET LAST DB UPDATE WHERE LAST DATE + HIGH RATING --> SEND TO RABBIT FOR EMAIL
                print(books)
        print(len(books))
        return books
#
# class BookUpdateServices()
#
#     def get_books_from_rabbit(self):
#         """
#         Реализация консьюмера RabbitMQ
#         :return:
#         """
#         ...
#
#     def buy_book(self, book_id, user_id):
#         pass
#
#     def prebook_book(selfself, book_id, user_id):
#         pass