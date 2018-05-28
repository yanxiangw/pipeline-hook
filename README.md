This is a serverless application for managing and monitoring AWS CodePipeline


## Dependency

- [Serverless](https://serverless.com/)
- [boto3](https://github.com/boto/boto3)

## Configuration

Application specific configuration are loaded using AWS SSM parameter store.
The parameters are prefixed with `/pipeline-hook/` by default. e.g.

```
/pipeline-hook/SLACK_WEBHOOK_URL
```

These can be configured in [AWS System Manager](https://ap-southeast-2.console.aws.amazon.com/systems-manager/home?region=ap-southeast-2)
The following parameters are needed for the application to work:

- **SLACK_WEBHOOK_URL** # slack channel webhook url to post message to
- **PIPELINE_NAME** # AWS CodePipeline name to listen to event from
- **FAVICON_URL** # favicon to be shown in slack message footer
- **APP_NAME** # app name to be displayed in slack message footer

## Deployment

```
serverless deploy
```