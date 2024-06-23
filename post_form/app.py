import json
import uuid

import boto3
from auth.utils import get_user_id
from cors.utils import add_cors_headers
from form.utils import serialize_form, validate_request_body

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    body = event.get("body")
    sub = get_user_id(event)

    if sub is not None:
        if not validate_request_body(event):
            return add_cors_headers({
                "statusCode": 400
            })

        json_body = json.loads(body)

        form_id = str(uuid.uuid4())
        form_tree_filename = f"{form_id}.json"

        new_item = {
            'owner': {
                'S': sub,
            },
            'id': {
                'S': form_id,
            },
            'name': {
                'S': json_body["name"],
            },
            'description': {
                'S': json_body["description"],
            }
        }

        dynamodb_client.put_item(
            Item=new_item,
            TableName='form-tree-app-forms',
        )

        s3_client.put_object(
            Body='[{"id": "root", "label": "Type the first question here", "children": []}]',
            Bucket="form-tree-app",
            Key=form_tree_filename,
        )

        return add_cors_headers({
            "statusCode": 201,
            "body": json.dumps(serialize_form(new_item)),
        })

    return add_cors_headers({
        "statusCode": 403
    })
