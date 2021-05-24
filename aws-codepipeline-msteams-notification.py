## AWS CodePipeline MS Teams Notification
# Original Author: https://github.com/globaldatanet/aws-codepipeline-notification
# Modified by: Seff Parker
# Modified Version: 1.0.2 20210524

import json
import logging
import os
import re
import urllib3
http = urllib3.PoolManager()

HOOK_URL = os.environ['WebhookUrl']


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    message = event

    logger.info("Message: " + str(message))

    # use data from logs
    pipeline = message['detail']['pipeline']
    if "AccountId" in os.environ:
        awsAccountId = os.environ['AccountId']
    else:
        awsAccountId = message['account']
    awsRegion = message['region']
    stage = message['detail']['stage']
    state = message['detail']['state']
    if 'external-execution-summary' in message['detail']['execution-result']:
        summary =  message['detail']['execution-result']['external-execution-summary']
    else:
        summary = "Nil"
    provider = message['detail']['type']['provider']
    
    # set the color depending on state
    if state == 'SUCCEEDED':
        color = "#00ff00"
    elif state == 'FAILED':
        color = "#ff0000"
    else:
         color = "#000000"
		
    # data for message cards
    title = pipeline    
    accountString = "Account"
    summaryString = "Summary"
    statusString = "Status"
    if 'external-execution-url' in message['detail']['execution-result']:
        pipelineURL =  message['detail']['execution-result']['external-execution-url']
    else:
        pipelineURL = f"https://{awsRegion}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline}/view?region={awsRegion}"
    
    # MS Teams data
    MSTeams = {
        "title": "%s" % title,
        "info": [ 
            { "facts":
                [{ "name": accountString, "value": awsAccountId },
                 { "name": statusString, "value": stage + " in " + provider + " has " + state },
                 { "name": summaryString, "value": summary }
                 ], "markdown": 'true' }
            ],
        "link": [
            { "@type": "OpenUri", "name": "Jump to " + provider, "targets":
                [
                    { "os": "default", "uri": pipelineURL }
                ]
            }
        ]
    }

    message_data = {
                "summary": "summary",
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "themeColor": color,
                "title": MSTeams["title"],
                "sections": MSTeams["info"],
                "potentialAction": MSTeams["link"]
            }
    
    # send message to webhook
    http.request('POST', HOOK_URL,
                 headers={'Content-Type': 'application/json'},
                 body=json.dumps(message_data))
