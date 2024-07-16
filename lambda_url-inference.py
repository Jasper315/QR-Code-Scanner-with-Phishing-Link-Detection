import boto3
import json
import re

url_regex = re.compile(
    r'^(?:http|ftp)s?://'  
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|' 
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
    r'(?::\d+)?' 
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
def lambda_handler(event, context):
    
    runtime_client = boto3.client('runtime.sagemaker')
    
    try:
        endpoint_name = 'GRP1-endpoint-2024-06-21-10-42-09'

        urltest = event['url']
        if not isinstance(urltest,str):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid URL format'})
            }
            
        if url_regex.match(urltest) is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid URL format'})
            }

        payload = json.dumps({"URL": urltest})
        response = runtime_client.invoke_endpoint(EndpointName=endpoint_name,
                                                ContentType="application/json",
                                                Body=payload)
        
        legit_perc = float(json.loads(response['Body'].read().decode('utf-8').rstrip()))

        if legit_perc > 0.75:
            legit_status = 1
        elif legit_perc < 0.25:
            legit_status = -1
        else:
            legit_status = 0

        val_return = json.dumps({"Legitimate": legit_perc, "Legitimate_Status": legit_status})

        # Return the result to the client
        return {
            'statusCode': 200,
            'body': val_return,
            'headers': {'content-type': 'application/json'}
        }

    except Exception as e:
        # Handle exceptions
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
