import requests

from tests.utils import BASE_URL


def test_delete_form_requires_authentication(test_data):
    forms, _ = test_data
    form_id = forms[0]["id"]
    response = requests.delete(f"{BASE_URL}/form/{form_id}")
    assert response.status_code == 403


def test_delete_form_non_existing_form_id(test_data):
    _, token = test_data

    form_id = "random-id"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{BASE_URL}/form/{form_id}", headers=headers)

    assert response.status_code == 204


def test_delete_form(test_data):
    forms, token = test_data

    form_id = forms[0]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.delete(f"{BASE_URL}/form/{form_id}", headers=headers)

    assert response.status_code == 204
