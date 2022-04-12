from typing import Optional

from sqlalchemy import select

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from book_service.application import interfaces
from book_service.application.dataclasses import Book
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

    def get_or_create(self, book: Book) -> Book:
        if book.book_id is None:
            self.add(book)
        else:
            new_book = self.get_by_id(book.book_id)
            if new_book is None:
                self.add(book)
            else:
                book = new_book
        return book

    # def update(self, book: Book):
    #     book_query = self.session.query(Book).filter_by(book_id=book.book_id).one_or_none()
    #     if not book_query:
    #         raise errors.NoBook(message="no book founded")
    #     if book.author_name is not None:
    #         book_query.author_name = book.author_name
    #     if book.book_title is not None:
    #         book_query.book_title = book.book_title
    #     self.session.flush()
    #     self.session.commit()
    #     return book_query

    def delete(self, book_id: int):
        book = self.session.query(Book).filter(Book.book_id == book_id).one_or_none()
        if not book:
            raise errors.NoBook(message="no book to delete")
        self.session.delete(book)

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
        selected_book = self.get_by_id(book_id)
        if selected_book is None:
            raise errors.NoBook(message="not valid ID of book")
        else:
            if selected_book.user_id is not None:
                if selected_book.user_id == user_id:
                    selected_book.user_id = None
                else:
                    raise errors.NoBook(message="you are not an owner of this book")
            else:
                raise errors.NoBook(message="book no need to be returned")

    def get_all(self):
        books = self.session.query(Book).order_by(Book.book_id).all()
        return books

    def get_user_books(self, user_id: int):
        selected_books = self.session.query(Book).where(Book.user_id == user_id).all()
        return selected_books

    def get_free_books(self):
        selected_books = self.session.query(Book).where(Book.user_id is None).order_by(Book.book_id).all()
        return selected_books
    
    def buy_book(self, book_id, user_id):
        pass

    def prebook_book(selfself, book_id, user_id):
        pass