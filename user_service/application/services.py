import logging
import sys
from typing import Optional

import jwt

from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component

from user_service.application import errors, interfaces
from user_service.application.dataclasses import User

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
root.addHandler(handler)

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    name: str
    email: str


class UserUpdate(DTO):
    name: Optional[str] = None
    email: Optional[str] = None
    id: Optional[int] = None


@component
class UsersService:
    user_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        new_user = user_info.create_obj(User)
        user = self.user_repo.get_or_create(new_user)

        token = jwt.encode(
            {
                "sub": user.id,
                "name": user.name,
                "email": user.email,
                "login": user.name,
                "group": "User"
            },
            'kerim_project',
            algorithm='HS256'
        )
        return token

    @join_point
    def get_user(self, id: int):
        user = self.user_repo.get_by_id(id)
        if user is None or user.id != id:
            raise errors.ErrorUser(message="No user exist")
        else:
            return user

    @join_point
    def message_sender(self, data: dict):
        users = self.user_repo.get_all()
        for user in users:
            root.info(
                f"attention user {user.name},\n "
                f"new books {data} arrived\n"
            )
        return data
