import os
import json
from urllib.parse import parse_qs
import util

def prompt(event):
    action = event["detail"]["action"]
    stage = event["detail"]["stage"]
    json_message = {
        "attachments": [
            {
                "pretext": f"Manual approval for AWS CodePipline {os.environ['PIPELINE_NAME']}",
                "title": f"{action} on {stage}",
                "color": "warning",
                "fields": [
                    {
                        "title": "Version",
                        "value": util.get_version(event["detail"]["execution-id"])
                    }
                ],
                "callback_id": "release_approval",
                "actions": [
                    {
                        "name": "action",
                        "text": "Approve",
                        "type": "button",
                        "value": "Approved",
                        "style": "primary"
                    },
                    {
                        "name": "action",
                        "text": "Reject",
                        "type": "button",
                        "value": "Rejected",
                        "style": "danger"
                    }
                ],
                "footer": os.environ["APP_NAME"],
                "footer_icon": os.environ["FAVICON_URL"]
            }
        ]
    }
    return 200, util.send(json_message)

def listen(event, context):
    print(f"Receive event: {event}")
    status, body = prompt(event)
    return { "statusCode": status, "body": body }
