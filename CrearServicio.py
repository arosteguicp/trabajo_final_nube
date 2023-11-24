import json
import boto3
def lambda_handler(event, context):
    
    cliente_id = event['cliente_id']
    mascota_id = event['mascota_id']
    servicio = event['servicio']
    duracion = event['duracion']
    
    dynamodb =boto3.resource('dynamodb')

        
    table= dynamodb.Table('servicios')
    table_clientes = dynamodb.Table('veterinarias')
    table_mascotas = dynamodb.Table('mascotas')
    
    # Verificar si el cliente existe
    cliente = table_clientes.get_item(Key={'cliente_id': cliente_id, 'tenant_id': tenant_id})
    if 'Item' not in cliente:
        return {
            'statusCode': 404,
            'message': 'El cliente no existe'
        }
    
    # Verificar si la mascota existe
    mascota = table_mascotas.get_item(Key={'mascota_id': mascota_id})
    if 'Item' not in mascota:
        return {
            'statusCode': 404,
            'message': 'La mascota no existe'
        }
        
    servicio_data = {
        'cliente_id' : cliente_id,
        'mascota_id' : mascota_id,
        'servicio' : servicio,
        'duracion' : duracion
        
    }
    
    table.put_item(Item=servicio_data)
    #salida
    return {
        'statusCode': 200,
        'Servicio registrado' : servicio_data
    }
