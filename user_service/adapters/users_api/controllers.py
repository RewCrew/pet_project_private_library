from user_service.application import services
from evraz.classic.components import component

from user_service.adapters.users_api.join_points import join_point
from falcon import Request, Response

from evraz.classic.http_auth import (
    authenticate,
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

    @authenticate
    @join_point
    def on_post_delete_user(self, requset: Request, response: Response):
        self.users.delete_user(requset.context.client.user_id)
        response.media = {'message': 'you are deleted from library'}

    @authenticate
    @join_point
    def on_post_update(self, requset: Request, response: Response):
        requset.media['id'] = requset.context.client.user_id
        self.users.update_user(**requset.media)
        response.media = {'message': 'user updated'}
