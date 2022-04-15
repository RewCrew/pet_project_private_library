import datetime
from typing import Optional, List

from sqlalchemy import select, or_

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository

from book_service.application import interfaces
from book_service.application.dataclasses import Book, UserBooks
from book_service.application import errors
from book_service.adapters.database import tables

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
            return_days = (datetime.date.today() - selected_book.return_date)
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
        selected_books = self.session.query(UserBooks).where(UserBooks.prebooked_by_user_id == user_id, UserBooks.booked_forever is not True).all()
        return selected_books

    def get_history_user_books(self, user_id:int):
        selected_books = self.session.query(UserBooks.book_isbn).where(UserBooks.user_id_history == user_id,
                                                             UserBooks.returned == True,
                                                             UserBooks.booked_forever == False).all()
        return selected_books

    def get_free_books(self):
        selected_books = self.session.query(Book).join(UserBooks.book_isbn == Book.isbn13).order_by(Book.book_id).all()
        return selected_books
    
    def buy_book(self, book_isbn, user_id):
        book = self.get_by_isbn_userbooks(book_isbn)
        if book is None:
            raise errors.NoBook(message='Book not booked buy you')
        else:
            if book.prebooked_by_user_id != user_id or book.finally_booked_by_user_id is not None:
                raise errors.NoBook(message='Book bought by someone else')
            else:
                book.prebooked_by_user_id = None
                book.finally_booked_by_user_id = user_id
                book.booked_forever = True
                book.return_date = datetime.date.today()
                return book


    def userbook_create(self, userbook:UserBooks):
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
            query = query.filter(tables.books.c.publisher.ilike(f'%{publisher}%'))
        if 'keyword' in filters:
            keyword = filters['keyword']
            query = query.filter(or_(tables.books.c.title.ilike(f'%{keyword}%'),
                                     tables.books.c.desc.ilike(f'%{keyword}%'),
                                     tables.books.c.subtitle.ilike(f'%{keyword}%')))
        return query

    @staticmethod
    def filter_price(filters: dict, query):
        if 'price' in filters:
            price = filters.pop('price')
            filt, value = price.split(':')
            if filt == 'lt':
                query = query.filter(tables.books.c.price < value)
            elif filt == 'gt':
                query = query.filter(tables.books.c.price > value)
            elif filt == 'lte':
                query = query.filter(tables.books.c.price <= value)
            elif filt == 'gte':
                query = query.filter(tables.books.c.price >= value)
            else:
                query = query.filter(tables.books.c.price == value)
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