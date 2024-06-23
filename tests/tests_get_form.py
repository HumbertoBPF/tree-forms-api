import requests

from tests.utils import BASE_URL


def test_get_form_requires_authentication(test_data):
    forms, _ = test_data
    form_id = forms[0]["id"]
    response = requests.get(f"{BASE_URL}/form/{form_id}")
    assert response.status_code == 403


def test_get_form_not_found(test_data):
    _, token = test_data
    form_id = "random-id"

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/form/{form_id}", headers=headers)

    assert response.status_code == 404


def test_get_form(test_data):
    forms, token = test_data
    form_id = forms[0]["id"]

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/form/{form_id}", headers=headers)

    assert response.status_code == 200

    response_body = response.json()

    assert "id" in response_body
    assert "owner" in response_body
    assert "name" in response_body
    assert "description" in response_body
    assert "form_tree" in response_body
