from evraz.classic.app.errors import AppError


class ErrorUser(AppError):
    msg_template = "Error recieved"
    code = 'user.error'
