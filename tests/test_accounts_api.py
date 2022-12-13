import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def api():
    from shopeat.api.asgi import app

    with TestClient(app) as api_client:
        yield api_client


def make_account_data():
    return {"email": "toto@example.com", "username": "toto", "password": "hello"}


def test_account_creation_and_authentication(api: TestClient):
    account_data = make_account_data()
    # create account
    response = api.post("/accounts", json=account_data)
    assert response.status_code == 200
    # get access token
    response = api.post(
        "/auth/token",
        json={
            "username": account_data["username"],
            "password": account_data["password"],
        },
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    # get current identity from access token
    response = api.get("/accounts/whoami", headers={"X-Api-Key": access_token})
    assert response.status_code == 200
    whoami_account = response.json()
    # compare whoami response to account_data
    assert len(whoami_account["uid"]) == 32
    assert whoami_account["email"] == account_data["email"]
    assert whoami_account["username"] == account_data["username"]
    assert whoami_account.get("password") is None


def test_get_token_with_wrong_credentials_raises_401(api: TestClient):
    account_data = make_account_data()
    response = api.post(
        "/auth/token",
        json={
            "username": account_data["username"],
            "password": account_data["password"],
        },
    )
    assert response.status_code == 401


def test_create_account_twice_raises_409(api: TestClient):
    account_data = make_account_data()
    response = api.post("/accounts", json=account_data)
    assert response.status_code == 200
    response = api.post("/accounts", json=account_data)
    assert response.status_code == 409
