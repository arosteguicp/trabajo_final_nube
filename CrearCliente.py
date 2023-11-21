import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    cliente_id = event['cliente_id']
    cliente_datos = event['cliente_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('veterinarias')
    cliente = {
        'tenant_id': tenant_id,
        'cliente_id': cliente_id,
        'cliente_datos': cliente_datos
    }
    response = table.put_item(Item=cliente)  		
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
