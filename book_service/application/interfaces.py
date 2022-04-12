from abc import ABC, abstractmethod
from .dataclasses import Book


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
    def delete(self, book_id: int):
        pass

    @abstractmethod
    def prebook_book(self, book_id: int, user_id: int):
        pass

    @abstractmethod
    def buy_book(self, book_id: int, user_id: int):
        pass

    @abstractmethod
    def return_book(self, book_id: int, user_id: int):
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
