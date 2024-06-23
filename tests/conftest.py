import pytest

from tests.utils import get_token, create_form, delete_forms


@pytest.fixture()
def test_data():
    token = get_token()
    forms = [
        create_form("name for form 1", "description for form 1", token),
        create_form("name for form 2", "description for form 2", token),
        create_form("name for form 3", "description for form 3", token)
    ]
    yield forms, token
    delete_forms([form["id"] for form in forms], token)

