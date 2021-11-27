import boto3
import json
from lib.response import AlexaResponse

def lambda_handler(request, context):
    print('**** Alexa Request ****')
    print(json.dumps(request))

    # Validate directive
    if 'directive' not in request:
        ar = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INVALID_DIRECTIVE',
                     'message': 'Missing key: directive, Is the request a valid Alexa Directive?'})
        return send_response(ar.get())

    # Validate payload version
    payload_version = request['directive']['header']['payloadVersion']
    if payload_version != '3':
        ar = AlexaResponse(
            name='ErrorResponse',
            payload={'type': 'INTERNAL_ERROR',
                     'message': 'This skill only supports Smart Home API version 3'})
        return send_response(ar.get())

    name = request['directive']['header']['name']
    namespace = request['directive']['header']['namespace']

    if namespace == 'Alexa.Authorization' and name == 'AcceptGrant':
        # grantee_token is used to identify your customer/user
        grantee_token = request['directive']['payload']['grantee']['token']
        # grant_code is used to get a token to send responses async
        grant_code = request['directive']['payload']['grant']['code']
        scope_token = 'TO-DO: What is the initial token for?'
        print(grant_code, grantee_token)
        ar = AlexaResponse(namespace='Alexa.Authorization', name='AcceptGrant.Response')

    elif namespace == 'Alexa.Discovery':
        scope_token = request['directive']['payload']['scope']['token']
        ar = AlexaResponse(name='DeferredResponse', payload={'estimatedDeferralInSeconds':7})
    
    else:
        correlation_token = request['directive']['header']['correlationToken']
        scope_token = request['directive']['endpoint']['scope']['token']
        endpoint_id = request['directive']['endpoint']['endpointId']
        ar = AlexaResponse(name='DeferredResponse', 
                payload={'estimatedDeferralInSeconds':7},
                endpoint_id=endpoint_id,
                correlation_token=correlation_token)
        
    topic, region = get_user(scope_token)
    client = boto3.client('iot-data', region_name=region)
    client.publish(
        topic='alexa/{}/request'.format(topic),
        qos=0,
        payload=json.dumps(request))
            
    response = ar.get()
    # Scope not needed for a deferred response
    response['event']['endpoint'].pop('scope')
    print('**** Lambda Handler Response ****')
    print(json.dumps(response))
    return response


def get_user(token):
    # from the token get a unique topic where to send the mssages to
    return 'edgewater', 'us-east-1'

