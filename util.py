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