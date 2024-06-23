import json

import boto3
from auth.utils import get_user_id
from cors.utils import add_cors_headers
from form.utils import serialize_form

client = boto3.client('dynamodb')


def lambda_handler(event, context):
    sub = get_user_id(event)

    if sub is not None:
        response = client.query(
            ExpressionAttributeNames={"#owner": "owner"},
            ExpressionAttributeValues={
                ':o': {
                    'S': sub,
                },
            },
            KeyConditionExpression='#owner = :o',
            TableName='form-tree-app-forms',
        )

        serialized_items = [serialize_form(item) for item in response["Items"]]

        return add_cors_headers({
            "statusCode": 200,
            "body": json.dumps({
                "items": serialized_items
            })
        })

    return add_cors_headers({
        "statusCode": 403
    })
