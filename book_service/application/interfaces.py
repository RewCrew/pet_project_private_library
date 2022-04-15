from abc import ABC, abstractmethod
from typing import Optional

from .dataclasses import Book, UserBooks


class BooksRepo(ABC):

    @abstractmethod
    def add(self, book: Book):
        pass

    @abstractmethod
    def get_or_create(self, book: Book):
        pass

    @abstractmethod
    def get_by_id(self, id_: int):
        pass

    @abstractmethod
    def get_by_isbn(self, isbn: int):
        pass

    @abstractmethod
    def get_by_isbn_userbooks(self, isbn: int):
        pass

    @abstractmethod
    def buy_book(self, book_isbn: int, user_id: int):
        pass

    @abstractmethod
    def return_book(self, book_isbn: int, user_id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_user_books(self, user_id: int):
        pass

    @abstractmethod
    def get_free_books(self):
        pass

    @abstractmethod
    def userbook_create(self, userbook: UserBooks):
        pass

    @abstractmethod
    def get_history_user_books(self, user_id: int):
        pass

    @abstractmethod
    def get_by_filter(self, filter_data: dict):
        pass
