import json

import boto3
from auth.utils import get_user_id
from cors.utils import add_cors_headers
from form.utils import validate_form_ids_in_request_body

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')


def get_delete_request_items(form_ids, sub):
    return [{
        "DeleteRequest": {
            "Key": {
                "owner": {
                    "S": sub,
                },
                "id": {
                    "S": form_id,
                },
            }
        }
    } for form_id in form_ids]


def lambda_handler(event, context):
    body = event.get("body")
    sub = get_user_id(event)

    if sub is not None:
        if validate_form_ids_in_request_body(event):
            json_body = json.loads(body)
            form_ids = json_body["form_ids"]

            dynamodb_client.batch_write_item(
                RequestItems={
                    'form-tree-app-forms': get_delete_request_items(form_ids, sub)
                },
            )

            s3_client.delete_objects(
                Bucket='form-tree-app',
                Delete={
                    'Objects': [{'Key': f"{form_id}.json"} for form_id in form_ids]
                },
            )

            return add_cors_headers({
                "statusCode": 204
            })

        return add_cors_headers({
            "statusCode": 400
        })

    return add_cors_headers({
        "statusCode": 403
    })
