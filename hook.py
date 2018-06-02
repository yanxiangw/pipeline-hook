import os
from pipeline import Pipeline
from slack import Slack

def is_relavant(detail):
  return detail["state"] == "FAILED" or detail["stage"] in ["Production", "Staging"]

def process(detail):
  slack = Slack(os.environ["APP_NAME"], os.environ["FAVICON_URL"])
  pipeline = Pipeline(os.environ['PIPELINE_NAME'])
  message = slack.build_message(pipeline.revision(detail["execution-id"]), os.environ['PIPELINE_NAME'], detail)
  return slack.send(os.environ["SLACK_WEBHOOK_URL"], message)

def listen(event, context):
  detail = event["detail"]
  body = process(detail) if is_relavant(detail) else "Irrelevant event received"
  return { "statusCode": 200, "body": body }
