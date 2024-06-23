import requests

from tests.utils import BASE_URL


def assert_form(form):
    assert "id" in form
    assert "owner" in form
    assert "name" in form
    assert "description" in form


def test_get_forms_requires_authentication():
    response = requests.get(f"{BASE_URL}/form")
    assert response.status_code == 403


def test_get_forms(test_data):
    _, token = test_data

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/form", headers=headers)

    response_body = response.json()

    items = response_body["items"]

    assert len(items) == 3

    for form in items:
        assert_form(form)
