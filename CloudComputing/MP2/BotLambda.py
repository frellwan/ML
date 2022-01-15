# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 06:19:26 2020

@author: frell
"""

import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MP2_CS498')

    intent = event.get('currentIntent')
    slots = intent.get('slots')
    source = slots.get('source')
    destination = slots.get('destination')

    try:
        response = table.get_item(
            Key={
                'source': source,
                'destination': destination
            }
        )
        
    except ClientError as e:
        print(e.response['Error']['Message'])
    
    
    if ('Item' not in response):
        if (source == destination):
            dist = 0
        else:
            dist = -1
        
        var1 = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "SSML",
                    "content": int(dist)
                },
            }
        }
        
    else:  
        item = response['Item']
        dist = json.dumps(item['distance'])
        var1 = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "SSML",
                    "content": int(item['distance'])
                },
            }
        }
    
    return var1