import requests

from tests.utils import BASE_URL, get_token, delete_forms


def test_post_form_requires_authentication():
    response = requests.post(f"{BASE_URL}/form")
    assert response.status_code == 403


def test_post_form_requires_name():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/form", json={
        "description": "Description for new form"
    }, headers=headers)
    assert response.status_code == 400


def test_post_form_requires_description():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/form", json={
        "name": "Name for new form"
    }, headers=headers)
    assert response.status_code == 400


def test_post_form():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    request_body = {
        "name": "Name for new form",
        "description": "Description for new form"
    }

    response = requests.post(f"{BASE_URL}/form", json=request_body, headers=headers)

    assert response.status_code == 201

    response_body = response.json()

    assert "id" in response_body
    assert "owner" in response_body
    assert response_body["name"] == request_body["name"]
    assert response_body["description"] == request_body["description"]

    delete_forms([response_body["id"]], token)
