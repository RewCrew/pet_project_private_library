from evraz.classic.app.errors import AppError


class NoUser(AppError):
    msg_template = "no user exist "
    code = 'user.not_member'
