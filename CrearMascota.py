import json
import boto3
import uuid # Importamos el modulo uuid

def lambda_handler(event, context):
    # Entrada (json)
    cliente_id = event['cliente_id']
    mascota_id = str (uuid.uuid4 ()) # Generamos un nuevo UUID aleatorio
    mascota_datos = event['mascota_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('mascotas')
    mascota = {
        'cliente_id': cliente_id,
        'mascota_id': mascota_id,
        'mascota_datos': mascota_datos
    }
    response = table.put_item(Item=mascota)  		
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
