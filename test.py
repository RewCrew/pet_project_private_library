import json
import requests



def get_books(params:list):
    books = []
    for param in params:
        for i in range(1,6):
            response = requests.get(f"https://api.itbook.store/1.0/search/{param}/{i}")
            result = response.content.decode("utf8")
            result = json.loads(result)
            if not result["books"]:
                break
            query = result["books"]
            for book in query:
                book['tag']=param
                books.append(book)
            print(books)
    print(len(books))
    return books

get_books(["mongo", "indesign"])

#
# def get_books_info(books):
#     for book in books: