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
