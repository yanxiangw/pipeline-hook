import json
import os
import urllib.request

class Slack:
  def __init__(self, app_name, icon_url):
    self.app_name = app_name
    self.icon_url = icon_url

  def build_message(self, revision, pipeline_name, detail):
    return {
      "attachments": [
        dict(self.__base_attachment(revision), **{
          "pretext": f"Update from AWS CodePipeline {pipeline_name}",
          "title": f"{detail['action']} on {detail['stage']} has {detail['state']}",
          "color": "good" if detail["state"] == "SUCCEEDED" else "danger",
        })
      ]
    }

  def build_prompt(self, revision, pipeline_name, detail):
    return {
      "attachments": [
        dict(self.__base_attachment(revision), **{
          "pretext": f"Manual approval for AWS CodePipline {pipeline_name}",
          "title": f"{detail['action']} on {detail['stage']}",
          "color": "warning",
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
          ]
        })
      ]
    }

  def send(self, webhook_url, message):
    print(f"Sending {message} to {webhook_url}")
    params = json.dumps(message).encode("utf8")
    req = urllib.request.Request(webhook_url,
      data=params,
      headers={"content-type": "application/json"})
    response = urllib.request.urlopen(req)
    return f"Response from Slack: {response.read().decode('utf8')}"

  def __base_attachment(self, revision):
    return {
      "fields": [{"title": "Version", "value": revision}],
      "footer": self.app_name,
      "footer_icon": self.icon_url
    }