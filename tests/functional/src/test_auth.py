import http


def test_registration(client):
    response = client.post(
        "/registration",
        json={
            "email": "testuser2@test.com",
            "password": "Password1",
        },
    )

    assert response.status_code == http.HTTPStatus.CREATED


def test_login(client):
    response = client.post(
        path="/login",
        json={
            "email": "testuser2@test.com",
            "password": "Password1",
        },
    )

    assert response.status_code == http.HTTPStatus.OK
    access_token = response.json.get("access_token")
    response = client.get(
        "/history", headers=dict(Authorization="Bearer " + access_token)
    )
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json.get("history")) == 1
