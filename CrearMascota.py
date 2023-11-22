import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    mascota_id = event['mascota_id']
    cliente_id = event['cliente_id']
    mascota_datos = event['mascota_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('mascotas')
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
