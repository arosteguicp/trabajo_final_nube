import json
import boto3
import uuid # Importar el módulo uuid
sns_client = boto3.client('sns')


def lambda_handler(event, context):
    
    cliente_id = event['cliente_id']
    mascota_id = event['mascota_id']
    servicio = event['servicio']
    duracion = event['duracion']
    tenant_id = event['tenant_id']
    
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
    mascota = table_mascotas.get_item(Key={'cliente_id': cliente_id, 'mascota_id': mascota_id})
    if 'Item' not in mascota:
        return {
            'statusCode': 404,
            'message': 'La mascota no existe'
        }
    else:    
        servicio_id = str (uuid.uuid4 ())
        
        servicio_data = {
            'cliente_id' : cliente_id,
            'servicio_id' : servicio_id,
            'mascota_id' : mascota_id,
            'servicio' : servicio,
            'duracion' : duracion
            
        }
    
        table.put_item(Item=servicio_data)
        	
        # Obtener el email de la veterinaria
        email = cliente['Item']['tenant_id']
        emailcorp = ("".join(email.split()) + "@gmail.com").lower()
        
        # Obtener el ARN del tema de SNS
        topic_arn = 'arn:aws:sns:us-east-1:851656937011:TemaNuevoServicio'
        
        # Verificar si la suscripción de tipo email existe para el tema de SNS
        response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
        subscription_arn = None
        for subscription in response['Subscriptions']:
            if subscription['Endpoint'] == emailcorp:
                subscription_arn = subscription['SubscriptionArn']
                break
        # Si no existe, crear una nueva
        if subscription_arn is None:
            response = sns_client.subscribe(TopicArn=topic_arn, Protocol='email', Endpoint=emailcorp)
            subscription_arn = response['SubscriptionArn']
        
        # Verificar si la suscripción está confirmada
        response = sns_client.get_subscription_attributes(SubscriptionArn=subscription_arn)
        # Si no está confirmada, esperar hasta que lo esté
        while response['Attributes']['SubscriptionArn'] == 'PendingConfirmation':
            response = sns_client.get_subscription_attributes(SubscriptionArn=subscription_arn)
        # Si está confirmada, obtener el ARN de la suscripción
        subscription_arn = response['Attributes']['SubscriptionArn']
        
        # Verificar si el filtro de tenant_id existe para la suscripción de tipo email
        response = sns_client.get_subscription_attributes(SubscriptionArn=subscription_arn)
        filter_policy = response['Attributes'].get('FilterPolicy')
        # Si no existe, crear uno nuevo
        if filter_policy is None or filter_policy != '{\"tenant_id\": [\"' + tenant_id + '\"]}':
            response = sns_client.set_subscription_attributes(SubscriptionArn=subscription_arn, AttributeName='FilterPolicy', AttributeValue='{\"tenant_id\": [\"' + tenant_id + '\"]}')

        response_sns = sns_client.publish(
    	TopicArn = topic_arn,
    	Subject = 'Nuevo Servicio',
        Message = json.dumps(servicio_data),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id }
            }
        )
        print(response_sns)
        
        #salida
        return {
            'statusCode': 200,
            'Servicio registrado' : servicio_data
        }
