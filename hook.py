import boto3
import json
import os
import urllib.request

def get_version(execution_id):
    client = boto3.client("codepipeline")
    response = client.get_pipeline_execution(
        pipelineName=os.environ["PIPELINE_NAME"],
        pipelineExecutionId=execution_id
    )
    return response["pipelineExecution"]["artifactRevisions"][0]["revisionSummary"]

def send(json_string):
    params = json.dumps(json_string).encode("utf8")
    req = urllib.request.Request(os.environ["SLACK_WEBHOOK_URL"],
        data=params,
        headers={"content-type": "application/json"})
    response = urllib.request.urlopen(req)
    return f"Response from Slack: {response.read().decode('utf8')}"

def slack_message(detail, time):
    title = f"{detail['action']} on {detail['stage']} has {detail['state']}"
    return {
        "attachments": [
            {
                "pretext": "Update from AWS CodePipeline",
                "title": title,
                "color": "good" if detail["state"] == "SUCCEEDED" else "danger",
                "fields": [
                    {
                        "title": "Version",
                        "value": get_version(detail["execution-id"])
                    }
                ],
                "footer": os.environ["APP_NAME"],
                "footer_icon": os.environ["FAVICON_URL"]
            }
        ]
    }

def process(event):
    status, body = 200, "Slack message is sent"
    detail, time = event["detail"], event["time"]
    if detail["state"] == "FAILED" or detail["stage"] in ["Production", "Staging"]:
        body = send(slack_message(detail, time))
    else:
        print("Other event received:", event)
        body = "Irrelevant event received"
    return status, body

def listen(event, context):
    status, body = process(event)
    return { "statusCode": status, "body": body }
