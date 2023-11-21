import json
import boto3
def lambda_handler(event, context):
    
    # TODO implement
    var_cliente_id = event['cliente_id']
    var_mascota_id = event['mascota_id']
    var_servicio = event['servicio']
    var_duracion = event['duracion']
    
    dynamodb =boto3.resource('dynamodb')

        
    table_servicios = dynamodb.Table('servicios')
    table_clientes = dynamodb.Table('clientes')
    table_mascotas = dynamodb.Table('mascotas')
    
    # Verificar si el cliente existe
    cliente = table_clientes.get_item(Key={'cliente_id': var_cliente_id})
    if 'Item' not in cliente:
        return {
            'statusCode': 400,
            'message': 'El cliente no existe'
        }
    
    # Verificar si la mascota existe
    mascota = table_mascotas.get_item(Key={'mascota_id': var_mascota_id})
    if 'Item' not in mascota:
        return {
            'statusCode': 400,
            'message': 'La mascota no existe'
        }
    servicio_data = {
        'cliente_id' : var_cliente_id,
        'mascota_id' : var_mascota_id,
        'servicio' : var_servicio,
        'duracion' : var_duracion
        
    }
    
    table.put_item(Item=servicio_data)
    #salida
    return {
        'statusCode': 200,
        'Servicio registrado' : servicio_data
    }
