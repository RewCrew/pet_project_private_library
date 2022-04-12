from evraz.classic.app.errors import AppError


class NoBook(AppError):
    msg_template = "book with id '{book.id}' doesnt exist"
    code = 'books.no_book'
