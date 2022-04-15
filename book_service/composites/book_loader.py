import json
from book_service.composites.app_api import Application as app

import requests


def get_books(params: list):
    app.books.get_books_from_api(params=params)


# def get_books(params:list):
#     books = []
#     for param in params:
#         for i in range(1,6):
#             response = requests.get(f"https://api.itbook.store/1.0/search/{param}/{i}")
#             result = response.content.decode("utf8")
#             result = json.loads(result)
#             if not result["books"]:
#                 break
#             query = result["books"]
#             for book in query:
#                 response = requests.get(f"https://api.itbook.store/1.0/books/{book['isbn13']}")
#                 result = response.content.decode("utf-8")
#                 result = json.loads(result)
#                 result['tag']=param
#                 books.append(result)
#             print(books)
#     print(len(books))
#     # for book in prebooks:
#     #     services.add_book(book)
#     # for isbn in prebooks:
#     #     response = requests.get(f"https://api.itbook.store/1.0/books/{isbn}")
#     #     result = response.content.decode("utf-8")
#     #     result = json.loads(result)
#     return books

#
# if __name__ == '__main__':
#     get_books(*sys.argv[1:])
