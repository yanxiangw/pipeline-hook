import os
import util

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
                        "value": util.get_version(detail["execution-id"])
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
        body = util.send(slack_message(detail, time))
    else:
        print("Other event received:", event)
        body = "Irrelevant event received"
    return status, body

def listen(event, context):
    status, body = process(event)
    return { "statusCode": status, "body": body }
