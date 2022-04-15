from evraz.classic.app.errors import AppError


class ErrorBook(AppError):
    msg_template = "Error recieved"
    code = 'books.trouble'
