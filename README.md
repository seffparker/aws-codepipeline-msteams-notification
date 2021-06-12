# AWS CodePipeline Teams Notification
Push AWS CodePipeline Notifications into Microsoft Teams as Webhook using AWS Lambda Function

This is an improved version of https://github.com/globaldatanet/aws-codepipeline-notification

# AWS Lambda Function
 - **Runtime:** Python 3.8
 - **Code:** aws-codepipeline-msteams-notification.py
 - **Environment Variables:** 

| KEY        | VALUE                    | SCOPE    |
|------------|--------------------------|----------|
| WebhookUrl | https://webhook_url_here | Required |
| AccountId  |      My AWS Account      | Optional |

# Amazon EventBridge (CloudWatch Events)
 - **Type:** Event Rule
 - **Event Pattern:** 
```
{
  "source": ["aws.codepipeline"],
  "detail-type": ["CodePipeline Action Execution State Change"],
  "detail": {
    "state": ["SUCCEEDED", "FAILED"]
  }
}
```
Only _Success_ and _Failures_ are included to avoid spamming. All the three stages _Source, Build,_ and _Deploy_ are included. You may adjust as required. 

# Microsoft Teams Incoming Webhook
Refer [here](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) to generate a WebHook URL for a Teams Channel.

# Sample Notification
![Sample Teams Notification](/codepipeline-teams-notification.png)
