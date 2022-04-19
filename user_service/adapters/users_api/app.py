import falcon
from . import controllers, auth
from evraz.classic.http_api import App
from evraz.classic.http_auth import Authenticator
from user_service.application import services


def create_app(
        is_dev_mode: bool,
        register: services.UsersService,
) -> App:
    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)

    if is_dev_mode:
        authenticator.set_strategies(auth.dummy_strategy)
    else:
        authenticator.set_strategies(auth.jwt_strategy)

    app = App(prefix='/api')

    app.register(controllers.Users(users=register, authenticator=authenticator))
    return app

