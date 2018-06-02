import os
import json
from urllib.parse import parse_qs

from lib.pipeline import Pipeline
from lib.slack import Slack

slack = Slack(os.environ["APP_NAME"], os.environ["FAVICON_URL"])
pipeline = Pipeline(os.environ['PIPELINE_NAME'])
webhook_url = os.environ["SLACK_WEBHOOK_URL"]

def is_relavant(detail):
  return detail["state"] == "FAILED" or detail["stage"] in os.environ["FILTER_STAGES"].split(',')

def listen(event, context):
  detail = event["detail"]
  if is_relavant(detail):
    message = slack.build_message(pipeline.revision(detail["execution-id"]), os.environ['PIPELINE_NAME'], detail)
    body = slack.send(webhook_url, message)
  else:
    body = "Irrelevant event received"
  return { "statusCode": 200, "body": body }

def review(event, context):
  detail = event["detail"]
  message = slack.build_prompt(pipeline.revision(detail["execution-id"]), os.environ['PIPELINE_NAME'], detail)
  body = slack.send(webhook_url, message)
  return { "statusCode": 200, "body": body }

def approve(event, context):
  pipeline = Pipeline(os.environ['PIPELINE_NAME'])
  payload = json.loads(parse_qs(event['body'])['payload'][0])
  status, body = pipeline.approve(payload["user"]["name"], payload["actions"][0]["value"])
  return { "statusCode": status, "body": body }