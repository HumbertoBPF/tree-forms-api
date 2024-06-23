import boto3
from auth.utils import get_user_id
from cors.utils import add_cors_headers

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    body = event.get("body")
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

        form_tree_filename = f"{form_id}.json"

        s3_client.put_object(
            Body=body,
            Bucket="form-tree-app",
            Key=form_tree_filename,
        )

        return add_cors_headers({
            "statusCode": 204,
        })

    return add_cors_headers({
        "statusCode": 403
    })