import json
import boto3
def lambda_handler(event, context):
    
    # TODO implement
    var_cliente_id = event['cliente_id']
    var_mascota_id = event['mascota_id']
    var_servicio = event['servicio']
    var_duracion = event['duracion']
    
    dynamodb =boto3.resource('dynamodb')
    table = dynamodb.Table('servicios')
    
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
