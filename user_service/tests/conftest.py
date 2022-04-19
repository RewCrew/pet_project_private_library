import pytest
from unittest.mock import Mock

from user_service.application import interfaces, dataclasses


@pytest.fixture(scope='function')
def user():
    return dataclasses.User(id=1, name='TestUser', email='TestEmail')


@pytest.fixture(scope='function')
def user2():
    return dataclasses.User(id=2, name='TestUser2', email='TestEmail2')


@pytest.fixture(scope='function')
def data():
    data = {
        'indesign': [
            {
                'error': '0',
                'title': 'Adobe Creative Cloud All-in-One For Dummies, 2nd Edition',
                'subtitle': 'Get ready to jump into the Creative Cloud',
                'authors': 'Jennifer Smith, Christopher Smith',
                'publisher': 'Wiley',
                'language': 'English',
                'isbn10': '1119420407',
                'isbn13': '9781119420408',
                'pages': '768',
                'year': '2017',
                'rating': '5',
                'desc': 'Adobe Creative Cloud is the most popular suite of tools among creative professionals, and a valuable resource you can use to fulfill all of your design goals. Ready to get started? The only book on the market of its kind, Adobe Creative Cloud All-in-One For Dummies is written by designers for design...',
                'price': 33.95,
                'image': 'https://itbook.store/img/books/9781119420408.png',
                'url': 'https://itbook.store/books/9781119420408'
            }, {
                'error': '0',
                'title': 'InDesign CS5 For Dummies',
                'subtitle': '',
                'authors': 'Galen Gruman',
                'publisher': 'Wiley',
                'language': 'English',
                'isbn10': '0470614498',
                'isbn13': '9780470614495',
                'pages': '460',
                'year': '2010',
                'rating': '4',
                'desc': 'As the industry standard in professional layout and design, InDesign delivers powerful publishing solutions for magazine, newspaper, and other publishing fields. This introductory book is an easy-to-understand reference for anyone migrating from another software application or those with little-to-n...',
                'price': 9.14,
                'image': 'https://itbook.store/img/books/9780470614495.png',
                'url': 'https://itbook.store/books/9780470614495'
            }, {
                'error': '0',
                'title': 'XML Publishing with Adobe InDesign',
                'subtitle': '',
                'authors': 'Dorothy Hoskins',
                'publisher': "O'Reilly Media",
                'language': 'English',
                'isbn10': '144939857X',
                'isbn13': '9781449398576',
                'pages': '111',
                'year': '2010',
                'rating': '4',
                'desc': 'From Adobe InDesign CS2 to InDesign CS5, the ability to work with XML content has been built into every version of InDesign. Some of the useful applications are importing database content into InDesign to create catalog pages, exporting XML that will be useful for subsequent publishing processes, an...',
                'price': 9.99,
                'image': 'https://itbook.store/img/books/9781449398576.png',
                'url': 'https://itbook.store/books/9781449398576'
            }
        ]
    }
    return data


@pytest.fixture(scope='function')
def users_repo(user, user2, data):
    users_repo = Mock(interfaces.UsersRepo)
    users_repo.get_or_create = Mock(return_value=user)
    users_repo.get_by_id = Mock(return_value=user)
    users_repo.get_all = Mock(return_value=[user, user2])
    users_repo.message_sender = Mock(return_value=data)
    return users_repo
