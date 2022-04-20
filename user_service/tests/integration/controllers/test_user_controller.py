import falcon
import jwt
import pytest


def test_register_user(users_service, client, user):
    users_service.add_user.return_value = jwt.encode(
        {
            "sub": user.id,
            "name": user.name,
            "email": user.email,
            "login": user.name,
            "group": "User"
        },
        'kerim_project',
        algorithm='HS256'
    )

    expected = {
        "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsIm"
        "5hbWUiOiJUZXN0VXNlciIsImVtYWlsIjoiVGVzdEVtYWlsIiwibG"
        "9naW4iOiJUZXN0VXNlciIsImdyb3VwIjoiVXNlciJ9.yVe28Ic2Tb"
        "NpY0uH4M3xPDLrFjyRjrv0i-XuOjtWAy4"
    }

    result = client.simulate_post(
        '/api/users/register',
        content_type=falcon.MEDIA_JSON,
        json={
            'name': 'TestUser',
            'email': 'TestEmail'
        }
    )
    assert result.status_code == 200
    assert result.json == expected


if __name__ == '__main__':
    pytest.main()