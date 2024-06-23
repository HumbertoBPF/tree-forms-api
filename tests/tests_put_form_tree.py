import uuid

import requests

from tests.utils import BASE_URL


def test_put_form_tree_requires_authentication():
    form_id = "random-id"
    response = requests.put(f"{BASE_URL}/form/{form_id}/form-tree")
    assert response.status_code == 403


def test_put_form_tree_not_found_form(test_data):
    _, token = test_data

    form_id = "random-id"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(f"{BASE_URL}/form/{form_id}/form-tree", headers=headers)

    assert response.status_code == 404


def test_put_form_tree(test_data):
    forms, token = test_data

    form_id = forms[0]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.put(f"{BASE_URL}/form/{form_id}/form-tree", json=[
        {
            "id": "root",
            "label": "Label root node",
            "children": [
                {
                    "id": str(uuid.uuid4()),
                    "label": "Label first child",
                    "children": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "label": "Label second child",
                    "children": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "label": "Label third child",
                    "children": []
                }
            ]
        }
    ], headers=headers)

    assert response.status_code == 204
