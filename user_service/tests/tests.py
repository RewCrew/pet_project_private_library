import pytest
from attr import asdict

from user_service.application import errors, services


@pytest.fixture(scope='function')
def user_test(users_repo):
    return services.UsersService(user_repo=users_repo)


test_data_user = {'id': 1, 'name': 'TestUser', 'email': 'TestEmail'}

test_data_user2 = {'id': 2, 'name': 'TestUser2', 'email': 'TestEmail2'}

test_data = {
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

wrong_test_data = {
    'mongo': [
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


def test_add_user(user_test):
    user_test.add_user(**test_data_user)
    user_test.user_repo.get_or_create.assert_called_once()
    user = user_test.user_repo.get_by_id(test_data_user['id'])
    assert test_data_user == asdict(user)


def test_get_user(user_test):
    user = user_test.user_repo.get_by_id(test_data_user['id'])
    assert asdict(user) == test_data_user


def test_get_wrong_user(user_test):
    with pytest.raises(errors.ErrorUser):
        user_test.get_user(5)


def test_get_all_users(user_test):
    users = user_test.user_repo.get_all()
    users = [asdict(user) for user in users]
    assert users == [test_data_user, test_data_user2]


def test_message_sender(user_test):
    message = user_test.message_sender(test_data)
    users = user_test.user_repo.get_all()
    users = [asdict(user) for user in users]
    assert users == [test_data_user, test_data_user2]
    assert message == test_data


def test_wrong_message_sender(user_test):
    message = user_test.message_sender(wrong_test_data)
    assert message != test_data
