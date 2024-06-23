import requests

from tests.utils import BASE_URL


def test_bulk_delete_form_requires_authentication():
    response = requests.delete(f"{BASE_URL}/form")
    assert response.status_code == 403


def test_bulk_delete_form_requires_form_ids(test_data):
    _, token = test_data
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/form", json={}, headers=headers)
    assert response.status_code == 400


def test_bulk_delete_form(test_data):
    forms, token = test_data

    headers = {"Authorization": f"Bearer {token}"}
    form_ids = [forms[0]["id"], forms[2]["id"]]

    response = requests.delete(f"{BASE_URL}/form", json={
        "form_ids": form_ids
    }, headers=headers)

    assert response.status_code == 204
