import boto3

client = boto3.client('dynamodb')
tablename = 'AddressMappings'
def storeMapping(user_id, mapping, address):
    exists = True
    try:
        current = client.get_item(
            TableName = tablename,
            Key={
                'user_id': {
                    'S': user_id
                }
            }
        )
    except:
        exists = False
    
    if not exists:
        response = client.put_item(
            TableName = tablename,
            Item={
                'user_id': {
                    'S': user_id
                }
                'mapping': {
                    M: {mapping : {"S" : address}}
                }
            }

        )
    # response = client.update_item(
    #     TableName = tablename,
    #     Key={
    #         'user_id': {
    #             'S': user_id
    #         }
    #     },
    )
