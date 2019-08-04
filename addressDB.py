import boto3

client = boto3.client('dynamodb')
tablename = 'AddressMappings'
def storeMapping(user_id, mapping, address):
    exists = True
    current = client.get_item(
        TableName = tablename,
        Key={
            'user_id': {
                'S': user_id
            }
        }
    )

    
    if 'Item' not in current:
        response = client.put_item(
            TableName = tablename,
            Item={
                'user_id': {
                    'S': user_id
                },
                'mappings': {
                    'L': [
                        {"M": {mapping: {"S": address}}}
                    ]
                }
            }

        )
    else:
        response = client.update_item(
            TableName = tablename,
            Key={
                'user_id': {
                    'S': user_id
                }
            },
            UpdateExpression='SET mappings = list_append(mappings, :address_obj)',
            ExpressionAttributeValues={
                ':address_obj':{
                    'L':[
                        {"M": {mapping: {"S": address}}}
                    ]
                }
            }

        )

