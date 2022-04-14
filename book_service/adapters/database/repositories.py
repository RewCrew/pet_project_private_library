import datetime
from typing import Optional

from sqlalchemy import select

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from book_service.application import interfaces
from book_service.application.dataclasses import Book, UserBooks
from book_service.application import errors


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):
    def add(self, book: Book):
        self.session.add(book)
        self.session.flush()
        self.session.refresh(book)
        return book

    def get_by_id(self, id_: int) -> Optional[Book]:
        query = select(Book).where(Book.book_id == id_)
        return self.session.execute(query).scalars().one_or_none()

    def get_by_isbn(self, isbn: int) -> Optional[Book]:
        query = select(Book).where(Book.isbn13 == isbn)
        return self.session.execute(query).scalars().one_or_none()

    def get_by_isbn_userbooks(self, isbn: int) -> Optional[UserBooks]:
        query = select(UserBooks).where(UserBooks.book_isbn == isbn, UserBooks.returned == False)
        return self.session.execute(query).scalars().one_or_none()

    def get_or_create(self, book: Book) -> Book:
        if book.isbn13 is None:
            self.add(book)
        else:
            new_book = self.get_by_isbn(book.isbn13)
            if new_book is None:
                self.add(book)
            else:
                book = new_book
        return book


    def take_book(self, book_id: int, user_id: int):
        selected_book = self.get_by_id(book_id)
        if selected_book is None:
            raise errors.NoBook(message="not valid ID of book")
        else:
            if selected_book.user_id is None:
                selected_book.user_id = user_id
                return selected_book
            else:
                raise errors.NoBook(message="book already taken")

    def return_book(self, book_id: int, user_id: int):
        selected_book = self.session.query(UserBooks).where(UserBooks.prebooked_by_user_id==user_id, UserBooks.returned==False).one_or_none()
        if selected_book is None:
            raise errors.NoBook(message="Book not ordered by you")
        else:
            return_days = (datetime.datetime.today() - selected_book.return_date)
            selected_book.prebooked_by_user_id = None
            selected_book.returned = True
            message = ("book returned")

            if return_days.days > 0:
                selected_book.prebooked_by_user_id = None
                selected_book.returned = True
                message = (f" user {user_id} please return book in time next time")
                return message
            return message



    def get_all(self):
        books = self.session.query(Book).order_by(Book.book_id).all()
        return books

    def get_user_books(self, user_id: int):
        selected_books = self.session.query(UserBooks).where(UserBooks.prebooked_by_user_id == user_id).all()
        return selected_books

    def get_history_user_books(self, user_id:int):
        selected_books = self.session.query(UserBooks.book_isbn).where(UserBooks.user_id_history == user_id,
                                                             UserBooks.returned == True,
                                                             UserBooks.booked_forever == False).all()
        return selected_books

    def get_free_books(self):
        selected_books = self.session.query(Book).where(Book.user_id is None).order_by(Book.book_id).all()
        return selected_books
    
    def buy_book(self, book_isbn, user_id):
        book = self.get_by_isbn(book_isbn)
        if book is None:
            raise errors.NoBook(message='no book exist')
        else:
            if book.prebooked_by_user_id == user_id:
                book.prebooked_by_user_id = None
                book.finally_booked_by_user_id = user_id
                return book
            else:
                raise errors.NoBook(message='book not prebooked by you')

    def prebook_book(self, book_isbn, user_id):
        book = self.get_by_isbn(book_isbn)
        if book is None:
            raise errors.NoBook(message='no book exist')
        else:
            if book.prebooked_by_user_id is not None or book.finally_booked_by_user_id is not None:
                raise errors.NoBook(message='Book ordered or bought by someone else')
            else:
                book.prebooked_by_user_id = user_id
                return book

    def userbook_create(self, userbook:UserBooks):
        self.session.add(userbook)
        self.session.flush()
