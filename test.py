import json
import requests

from heapq import nlargest

def get_books(params:list):
    # books = []
    # for param in params:
    #     for i in range(1,6):
    #         response = requests.get(f"https://api.itbook.store/1.0/search/{param}/{i}")
    #         result = response.content.decode("utf8")
    #         result = json.loads(result)
    #         if not result["books"]:
    #             break
    #         query = result["books"]
    #         for book in query:
    #             book['tag']=param
    #             books.append(book)
    # print(books)
    #
    # return books
    #

    books = {}
    for param in params:
        books[param] = []
        for i in range(1,6):
            result = requests.get(f"https://api.itbook.store/1.0/search/{param}/{i}").json()
            # result = response.content.decode("utf8")
            # result = json.loads(result)
            if not result["books"]:
                break
            query = result["books"]
            for book in query:
                response = requests.get(f"https://api.itbook.store/1.0/books/{book['isbn13']}")
                result = response.content.decode("utf-8")
                result = json.loads(result)
                # result['tag'] = param
                books[param].append(result)
            print(books)
    # print(len(books))
    return books
final_books = []
books = get_books(["indesign", 'mongo'])

# for book in books.values():
#     filtered_books = sorted(book, key = lambda x: x['rating'], reverse=True)
#     final_books.append(filtered_books[:3])
# print(final_books)
new_test = {'indesign': [{'error': '0', 'title': 'Adobe Creative Cloud All-in-One For Dummies, 2nd Edition', 'subtitle': 'Get ready to jump into the Creative Cloud', 'authors': 'Jennifer Smith, Christopher Smith', 'publisher': 'Wiley', 'language': 'English', 'isbn10': '1119420407', 'isbn13': '9781119420408', 'pages': '768', 'year': '2017', 'rating': '5', 'desc': 'Adobe Creative Cloud is the most popular suite of tools among creative professionals, and a valuable resource you can use to fulfill all of your design goals. Ready to get started? The only book on the market of its kind, Adobe Creative Cloud All-in-One For Dummies is written by designers for design...', 'price': '$33.95', 'image': 'https://itbook.store/img/books/9781119420408.png', 'url': 'https://itbook.store/books/9781119420408'}, {'error': '0', 'title': 'InDesign CS5 For Dummies', 'subtitle': '', 'authors': 'Galen Gruman', 'publisher': 'Wiley', 'language': 'English', 'isbn10': '0470614498', 'isbn13': '9780470614495', 'pages': '460', 'year': '2010', 'rating': '4', 'desc': 'As the industry standard in professional layout and design, InDesign delivers powerful publishing solutions for magazine, newspaper, and other publishing fields. This introductory book is an easy-to-understand reference for anyone migrating from another software application or those with little-to-n...', 'price': '$9.14', 'image': 'https://itbook.store/img/books/9780470614495.png', 'url': 'https://itbook.store/books/9780470614495'}, {'error': '0', 'title': 'XML Publishing with Adobe InDesign', 'subtitle': '', 'authors': 'Dorothy Hoskins', 'publisher': "O'Reilly Media", 'language': 'English', 'isbn10': '144939857X', 'isbn13': '9781449398576', 'pages': '111', 'year': '2010', 'rating': '5', 'desc': 'From Adobe InDesign CS2 to InDesign CS5, the ability to work with XML content has been built into every version of InDesign. Some of the useful applications are importing database content into InDesign to create catalog pages, exporting XML that will be useful for subsequent publishing processes, an...', 'price': '$9.99', 'image': 'https://itbook.store/img/books/9781449398576.png', 'url': 'https://itbook.store/books/9781449398576'}]}
for k,v in books.items():
    filter = sorted(v, key = lambda x: (-int(x['rating']), x['year']))
    books[k]=filter[:3]
    print(books)


# for k,v in books.items():
#     filter = sorted(v, key = itemgetter ('rating', 'year'), reverse=True)
#     books[k]=filter[:3]
#     print(books)
# books = sorted(books, key = lambda x: x['rating'], reverse=True)
# print(books[:3])
#
# lists = {'tag':[]}
# lists["tag"].append({'book':'book'})
# lists["tag"].append(({'newbook':'newbook'}))
# print(lists)