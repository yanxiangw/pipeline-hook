import os
import json
from urllib.parse import parse_qs
from pipeline import Pipeline
from slack import Slack

def process(detail):
  slack = Slack(os.environ["APP_NAME"], os.environ["FAVICON_URL"])
  pipeline = Pipeline(os.environ['PIPELINE_NAME'])
  message = slack.build_prompt(pipeline.revision(detail["execution-id"]), os.environ['PIPELINE_NAME'], detail)
  return slack.send(os.environ["SLACK_WEBHOOK_URL"], message)

def listen(event, context):
  body = process(event["detail"])
  return { "statusCode": 200, "body": body }

def respond(event, context):
  pipeline = Pipeline(os.environ['PIPELINE_NAME'])
  payload = json.loads(parse_qs(event['body'])['payload'][0])
  status, body = pipeline.approve(payload["user"]["name"], payload["actions"][0]["value"])
  return { "statusCode": status, "body": body }