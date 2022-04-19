from user_service.application import services
from evraz.classic.components import component

from user_service.adapters.users_api.join_points import join_point
from falcon import Request, Response

from evraz.classic.http_auth import (
    authenticator_needed,
)


@authenticator_needed
@component
class Users:
    users: services.UsersService

    @join_point
    def on_post_register(self, request: Request, response: Response):
        token = self.users.add_user(**request.media)
        response.media = {"Token": token}
