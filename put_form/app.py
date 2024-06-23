import json

import boto3
from auth.utils import get_user_id
from botocore.exceptions import ClientError
from cors.utils import add_cors_headers
from form.utils import serialize_form, validate_request_body

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    body = event.get("body")
    form_id = event["pathParameters"]["id"]
    sub = get_user_id(event)

    if sub is not None:
        if not validate_request_body(event):
            return add_cors_headers({
                "statusCode": 400
            })

        json_body = json.loads(body)

        updated_item = {
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

        try:
            client.put_item(
                Item=updated_item,
                TableName='form-tree-app-forms',
                ExpressionAttributeValues={':id': {
                    "S": form_id
                }},
                ExpressionAttributeNames={"#id": "id"},
                ConditionExpression="#id=:id"
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return add_cors_headers({
                    "statusCode": 404
                })

            raise e

        return add_cors_headers({
            "statusCode": 200,
            "body": json.dumps(serialize_form(updated_item)),
        })

    return add_cors_headers({
        "statusCode": 403
    })
