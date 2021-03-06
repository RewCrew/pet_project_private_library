from typing import List, Optional

from sqlalchemy import or_, select

from classic.components import component
from classic.sql_storage import BaseRepository

from book_service.adapters.database import tables
from book_service.application import interfaces
from book_service.application.dataclasses import Book, UserBooks


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
        query = select(UserBooks).where(
            UserBooks.book_isbn == isbn, UserBooks.returned == False
        )
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

    def return_book(self, book_id: int, user_id: int):
        selected_book = self.session.query(UserBooks).where(
            UserBooks.prebooked_by_user_id == user_id,
            UserBooks.returned == False
        ).one_or_none()
        return selected_book

    def get_all(self):
        books = self.session.query(Book).order_by(Book.book_id).all()
        return books

    def get_user_books(self, user_id: int):
        selected_books = self.session.query(UserBooks).where(
            UserBooks.prebooked_by_user_id == user_id, UserBooks.booked_forever
            is not True
        ).all()
        return selected_books

    def get_history_user_books(self, user_id: int):
        selected_books = self.session.query(UserBooks.book_isbn).where(
            UserBooks.user_id_history == user_id, UserBooks.returned == True,
            UserBooks.booked_forever == False
        ).all()
        return selected_books

    def get_free_books(self):
        selected_books = self.session.query(Book).join(
            UserBooks.book_isbn == Book.isbn13
        ).order_by(Book.book_id).all()
        return selected_books

    def buy_book(self, book_isbn, user_id):
        book = self.get_by_isbn_userbooks(book_isbn)
        return book

    def userbook_create(self, userbook: UserBooks):
        self.session.add(userbook)
        self.session.flush()

    def get_by_filter(self, filter_data: dict) -> Optional[List[Book]]:
        query = self.session.query(tables.books)
        query = self.default_filters(filter_data, query)
        query = self.filter_price(filter_data, query)
        query = self.sort_order_by(filter_data, query)
        return query.all()

    @staticmethod
    def default_filters(filters: dict, query):
        if 'authors' in filters:
            authors = filters['authors']
            if isinstance(filters['authors'], list):
                authors = ','.join(authors)
            query = query.filter(tables.books.c.authors.ilike(f'%{authors}%'))
        if 'publisher' in filters:
            publisher = filters['publisher']
            query = query.filter(
                tables.books.c.publisher.ilike(f'%{publisher}%')
            )
        if 'keyword' in filters:
            keyword = filters['keyword']
            query = query.filter(
                or_(
                    tables.books.c.title.ilike(f'%{keyword}%'),
                    tables.books.c.desc.ilike(f'%{keyword}%'),
                    tables.books.c.subtitle.ilike(f'%{keyword}%')
                )
            )
        return query

    @staticmethod
    def filter_price(filters: dict, query):
        if ('min_price' in filters) and ('max_price' in filters):
            min_price = filters.get('min_price')
            max_price = filters.get('max_price')
            query = query.filter(
                tables.books.c.price >= min_price,
                tables.books.c.price <= max_price
            )
        elif 'min_price' in filters:
            min_price = filters.pop('min_price')
            query = query.filter(tables.books.c.price >= min_price)
        elif 'max_price' in filters:
            max_price = filters.pop('max_price')
            query = query.filter(tables.books.c.price <= max_price)

        return query

    @staticmethod
    def sort_order_by(filters: dict, query):
        if 'order_by' in filters:
            order_by = filters.pop('order_by')
            filt, value = order_by.split(':')
            if filt == 'price':
                if value == 'desc':
                    query = query.order_by(tables.books.c.price.desc())
                else:
                    query = query.order_by(tables.books.c.price.asc())
            elif filt == 'pages':
                if value == 'desc':
                    query = query.order_by(tables.books.c.pages.desc())
                else:
                    query = query.order_by(tables.books.c.pages.asc())
        return query
