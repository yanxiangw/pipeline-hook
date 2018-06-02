import boto3

class Pipeline:
  def __init__(self, name):
    self.name = name
    self.client = boto3.client("codepipeline")

  def revision(self, execution_id):
    response = self.client.get_pipeline_execution(
      pipelineName=self.name,
      pipelineExecutionId=execution_id
    )
    return response["pipelineExecution"]["artifactRevisions"][0]["revisionSummary"]

  def approve(self, user, approval):
    stage, action, token = self.__current_state()
    self.client.put_approval_result(
      pipelineName=self.name,
      stageName=stage,
      actionName=action,
      result={
        'summary': f"{approval} by {user}",
        'status': approval
      },
      token=token
    )
    return 200, f"{approval} by {user}"

  def __current_state(self):
    response = self.client.get_pipeline_state(name=self.name)
    current_stage = self.__find_current(response["stageStates"])
    current_action = self.__find_current(current_stage["actionStates"])
    return current_stage["stageName"], current_action["actionName"], current_action["latestExecution"]["token"]

  def __find_current(self, steps):
    current_steps = [step for step in steps if step["latestExecution"]["status"] == "InProgress"]
    return current_steps[0] if current_steps else None