from abc import ABC, abstractmethod

from user_service.application.dataclasses import User


class UsersRepo(ABC):
    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def get_or_create(self, user: User):
        pass

    @abstractmethod
    def get_by_id(self, id_: int):
        pass

    @abstractmethod
    def delete(self, user_id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

