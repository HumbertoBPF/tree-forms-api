import boto3
import requests
import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = "http://localhost:8000"


def get_token():
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            "USERNAME": os.getenv("TEST_USER_USERNAME"),
            "PASSWORD": os.getenv("TEST_USER_PASSWORD")
        },
        ClientId=os.getenv("USER_POOL_CLIENT_ID"),
    )
    return response["AuthenticationResult"]["IdToken"]


def create_form(name, description, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/form", json={
        "name": name,
        "description": description
    }, headers=headers)
    return response.json()


def delete_forms(form_ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    requests.delete(f"{BASE_URL}/form", json={
        "form_ids": form_ids
    }, headers=headers)
