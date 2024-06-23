import boto3
from auth.utils import get_user_id
from cors.utils import add_cors_headers

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    form_id = event["pathParameters"]["id"]
    sub = get_user_id(event)

    if sub is not None:
        dynamodb_client.delete_item(
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

        s3_client.delete_object(
            Bucket='form-tree-app',
            Key=f"{form_id}.json",
        )

        return add_cors_headers({
            "statusCode": 204
        })

    return add_cors_headers({
        "statusCode": 403
    })
