# Crear
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
# Listar
import boto3  # import Boto3
from boto3.dynamodb.conditions import Key  # import Boto3 conditions

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('veterinarias')
    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id)
    )
    items = response['Items']
    num_reg = response['Count']
    # Salida (json)
    return {
        'statusCode': 200,
        'tenant_id':tenant_id,
        'num_reg': num_reg,
        'clientes': items
    }

# Modificar
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    cliente_id = event['cliente_id']
    cliente_datos = event['cliente_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('veterinarias')
    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'cliente_id': cliente_id
        },
        UpdateExpression="set cliente_datos=:cliente_datos",
        ExpressionAttributeValues={
            ':cliente_datos': cliente_datos
        },
        ReturnValues="UPDATED_NEW"
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
# Eliminar
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    cliente_id = event['cliente_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('veterinarias')
    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'cliente_id': cliente_id
        }
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
