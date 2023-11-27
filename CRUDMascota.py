# Crear
import json
import boto3
import uuid # Importar el módulo uuid

def lambda_handler(event, context):
    # Entrada (json)
    cliente_id = event['cliente_id']
    tenant_id = event['tenant_id']
    mascota_datos = event['mascota_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('veterinarias')
    # Verificar si el cliente existe en la tabla veterinarias
    response = table.get_item(Key={'cliente_id': cliente_id, 'tenant_id': tenant_id})
    if 'Item' not in response:
        # Si no existe, devolver un mensaje de error
        return {'statusCode': 404, 'message': 'Cliente no encontrado'}
    else:
        # Si existe, generar el mascota_id y consultar la tabla mascotas
        table = dynamodb.Table('mascotas')
        mascota_id = str (uuid.uuid4 ()) # Generar un nuevo UUID aleatorio y convertirlo a una cadena
        mascota = {
            'mascota_id': mascota_id,
            'cliente_id': cliente_id,
            'mascota_datos': mascota_datos
        }
        response = table.put_item(Item=mascota)  		
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
    cliente_id = event['cliente_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('mascotas')
    response = table.query(
        KeyConditionExpression=Key('cliente_id').eq(cliente_id)
    )
    items = response['Items']
    num_reg = response['Count']
    # Salida (json)
    return {
        'statusCode': 200,
        'cliente_id':cliente_id,
        'num_reg': num_reg,
        'mascotas': items
    }
# Modificar
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    cliente_id = event['cliente_id']
    mascota_id = event['mascota_id']
    mascota_datos = event['mascota_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('mas')
    response = table.update_item(
        Key={
            'cliente_id': cliente_id,
            'mascota_id': mascota_id
        },
        UpdateExpression="set mascota_datos=:mascota_datos",
        ExpressionAttributeValues={
            ':mascota_datos': mascota_datos
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
    cliente_id = event['cliente_id']
    mascota_id = event['mascota_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('mascotas')
    response = table.delete_item(
        Key={
            'cliente_id': cliente_id,
            'mascota_id': mascota_id
        }
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
