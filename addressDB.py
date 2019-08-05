import boto3

client = boto3.client('dynamodb')
tablename = 'AddressMappings'
def storeMapping(user_id, mapping, address):
    print(mapping, address)
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
def getMapping(user_id, mapping):
    response = client.get_item(
        TableName = tablename,
        Key={
            'user_id': {
                'S': user_id
            }
        }
    )
    if 'Item' not in response:
        return 1
    mappings = response['Item']['mappings']['L']
    try:
        address = None
        for i in mappings:
            if mapping in i['M']:
                address = i['M'][mapping]
        if address is not None:
            return address['S']
        else:
            return 2 
    except:
        return 3


