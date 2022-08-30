import http


def test_roles_list(client):
    response = client.post(
        "/roles",
        json={},
    )

    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json.get("roles")) > 0


def test_crud_role(client):
    response = client.post("/roles", json={"role": "test_role"})

    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json.get("result").get("role") == "test_role"

    response = client.post("/roles", json={"role": "test_role", "rights": [{"url": "/test_address"}]})
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json.get("result").get("rights")[0].get("url") == "/test_address"

    response = client.post("/roles", json={"role": "test_role", "deleted": True})
    assert response.status_code == http.HTTPStatus.OK


def test_user_role(client):
    client.post(
        "/registration",
        json={
            "email": "testuserrole@test.com",
            "password": "pass",
        },
    )

    response = client.post("/user_roles", json={"email": "testuserrole@test.com"})
    print(response.json)
    assert response.status_code == http.HTTPStatus.OK
    roles = [role["role"] for role in response.json.get("roles")]
    assert "regular" in roles

    response = client.post("/user_roles", json={"email": "testuserrole@test.com", "roles": [{"role": "subscriber"}]})
    assert response.status_code == http.HTTPStatus.CREATED

    response = client.post("/user_roles", json={"email": "testuserrole@test.com"})
    roles = [role["role"] for role in response.json.get("roles")]
    assert "subscriber" in roles
