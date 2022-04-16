import datetime
import json
from typing import Optional

import requests
from pydantic import validate_arguments

from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher

from book_service.application import errors

from . import interfaces
from .dataclasses import Book, UserBooks

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
    price: float
    image: str
    url: str
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
    @validate_arguments
    def add_book(self, data: dict):
        book_info = BookInfo(**data)
        new_book = book_info.create_obj(Book)
        book = self.books_repo.get_or_create(new_book)
        self.books_repo.add(book)

    @join_point
    @validate_arguments
    def return_book(self, book_isbn: int, user_id: int):
        book = self.books_repo.return_book(book_isbn, user_id)
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
    @validate_arguments
    def get_book(self, book_isbn: int):
        book = self.books_repo.get_by_isbn(book_isbn)
        if book is None or book_isbn != book.isbn13:
            raise errors.ErrorBook(message="No book exist")
        else:
            return book

    @join_point
    @validate_arguments
    def buy_book(self, book_isbn: int, user_id: int):
        book = self.books_repo.buy_book(book_isbn, user_id)
        return book

    @join_point
    @validate_arguments
    def prebook_book(
        self, book_isbn: int, user_id: int, order_for_days: Optional[int] = 7
    ):
        book = self.books_repo.get_by_isbn(book_isbn)
        if book is None:
            raise errors.ErrorBook(message="not valid ID of book")
        userbook = UserBooks(
            book_isbn=book.isbn13,
            booked_date=datetime.date.today(),
            prebooked_by_user_id=user_id,
            user_id_history=user_id,
            order_for_days=order_for_days,
            return_date=datetime.date.today() +
            datetime.timedelta(order_for_days),
            returned=False
        )
        book = self.books_repo.get_by_isbn_userbooks(book_isbn)
        if book is None:
            self.books_repo.userbook_create(userbook)
        else:
            if book.prebooked_by_user_id is None and book.finally_booked_by_user_id is None:
                userbook = self.books_repo.userbook_create(userbook)
                return userbook
            else:
                raise errors.ErrorBook(
                    message='you cant take this book, already booked or bought'
                )

    @join_point
    @validate_arguments
    def get_books_from_api(self, params: list):
        books = {}
        for param in params:
            books[param] = []
            for i in range(1, 6):
                response = requests.get(
                    f"https://api.itbook.store/1.0/search/{param}/{i}"
                )
                result = response.content.decode("utf8")
                result = json.loads(result)
                if not result["books"]:
                    break
                query = result["books"]
                for book in query:
                    response = requests.get(
                        f"https://api.itbook.store/1.0/books/{book['isbn13']}"
                    )
                    result = response.content.decode("utf-8")
                    result = json.loads(result)
                    books[param].append(result)
                    result['price'] = float(result['price'][1:])
                    self.publisher.publish(
                        Message("Exchange", {'data': result})
                    )
        for k, v in books.items():
            filter = sorted(v, key=lambda x: (-int(x['rating']), x['year']))
            books[k] = filter[:3]
        self.publisher.publish(Message("BookExchange", {"data": books}))
        return books

    @join_point
    @validate_arguments
    def get_history_user_books(self, user_id: int):
        books = self.books_repo.get_history_user_books(user_id)
        return books

    @join_point
    @validate_arguments
    def filter_books(self, filters: dict):
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')
        if (min_price is not None and (not min_price.isdigit())) \
                or (max_price is not None and (not max_price.isdigit())):
            raise errors.ErrorBook(
                message='wrong filters, please check your spelling'
            )
        result = self.books_repo.get_by_filter(filters)
        return result
