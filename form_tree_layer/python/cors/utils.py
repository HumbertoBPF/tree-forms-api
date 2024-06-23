def add_cors_headers(response):
    return {
        **response,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'POST,GET,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Credentials': True
        }
    }
