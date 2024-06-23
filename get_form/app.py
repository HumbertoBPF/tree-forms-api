import json

import boto3
from auth.utils import get_user_id
from botocore.exceptions import ClientError
from cors.utils import add_cors_headers
from form.utils import serialize_form

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    sub = get_user_id(event)
    form_id = event["pathParameters"]["id"]

    if sub is not None:
        response_dynamodb = dynamodb_client.get_item(
            Key={
                'owner': {
                    'S': sub,
                },
                'id': {
                    'S': form_id,
                },
            },
            TableName='form-tree-app-forms',
        )

        if "Item" not in response_dynamodb:
            return add_cors_headers({
                "statusCode": 404
            })

        item = response_dynamodb["Item"]
        serialized_items = serialize_form(item)

        try:
            response_s3 = s3_client.get_object(
                Bucket='form-tree-app',
                Key=f"{form_id}.json",
            )
            form_tree = response_s3['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchKey':
                raise e
            form_tree = "[]"

        return add_cors_headers({
            "statusCode": 200,
            "body": json.dumps({
                **serialized_items,
                "form_tree": json.loads(form_tree)
            })
        })

    return add_cors_headers({
        "statusCode": 403
    })
