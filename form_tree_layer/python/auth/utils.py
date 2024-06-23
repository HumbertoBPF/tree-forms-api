import jwt


def get_user_id(event):
    headers = event["headers"]
    auth_header = headers.get("Authorization")

    if auth_header is None:
        return None

    token = auth_header.replace("Bearer ", "")
    payload = jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})
    return payload.get("sub")
