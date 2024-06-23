import requests

from tests.utils import BASE_URL


def test_put_form_requires_authentication(test_data):
    forms, _ = test_data
    form_id = forms[0]["id"]
    response = requests.put(f"{BASE_URL}/form/{form_id}")
    assert response.status_code == 403


def test_put_form_requires_name(test_data):
    forms, token = test_data

    form_id = forms[0]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(f"{BASE_URL}/form/{form_id}", json={
        "name": "Updated name"
    }, headers=headers)

    assert response.status_code == 400


def test_put_form_requires_description(test_data):
    forms, token = test_data

    form_id = forms[0]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(f"{BASE_URL}/form/{form_id}", json={
        "description": "Updated description"
    }, headers=headers)

    assert response.status_code == 400


def test_put_form_not_found(test_data):
    forms, token = test_data

    form_id = "random-id"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(f"{BASE_URL}/form/{form_id}", json={
        "name": "Updated name",
        "description": "Updated description"
    }, headers=headers)

    assert response.status_code == 404


def test_put_form(test_data):
    forms, token = test_data

    form_id = forms[0]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    request_body = {
        "name": "Updated name",
        "description": "Updated description"
    }

    response = requests.put(f"{BASE_URL}/form/{form_id}", json=request_body, headers=headers)

    assert response.status_code == 200

    response_body = response.json()

    assert "id" in response_body
    assert "owner" in response_body
    assert response_body["name"] == request_body["name"]
    assert response_body["description"] == request_body["description"]
