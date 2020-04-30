import uuid
import logging

import stepfunctions
from stepfunctions import steps
from stepfunctions.inputs import ExecutionInput
from stepfunctions.workflow import Workflow

stepfunctions.set_stream_logger(level=logging.INFO)
id = uuid.uuid4().hex

FLOW_NAME='active_learning_flow_{}'.format(id)
WORKFLOW_ROLE='ROLE ARN'

if __name__ == '__main__':
    # SFn の実行に必要な情報を渡す際のスキーマを定義します
    execution_input = ExecutionInput(
        schema={
            # AWS Batch
            'BatchJobDefinition': str,
            'BatchJobName': str,
            'BatchJobQueue': str,
        
            # AWS Lambda
            'LambdaFunctionName': str,
        }
    )

    # SFn のワークフローの定義を記載します
    inputs={
        # AWS Batch
        'BatchJobDefinition': 'active-learning-job_run:1',
        'BatchJobName': 'active-learning-inference',
        'BatchJobQueue': 'active-learning-inference',

        # AWS Lambda
        'LambdaFunctionName': 'create_labeling_job'
    }
    
    ## AWS Batch のジョブを Submit するステップ
    inference_step = steps.BatchSubmitJobStep(
        'Execute AWS Batch job',
        parameters={
            "JobDefinition":execution_input['BatchJobDefinition'],
            "JobName": execution_input['BatchJobName'],
            "JobQueue": execution_input['BatchJobQueue'] 
        }
    )
    
    ## AWS Lambda のジョブを Submit するステップ
    lambda_step = steps.compute.LambdaStep(
        'Create Labeling job',
        parameters={"FunctionName": execution_input['LambdaFunctionName']}
    )
    
    # 各 Step を連結
    chain_list = [inference_step, lambda_step]
    workflow_definition = steps.Chain(chain_list)
    
    # Workflow の作成
    workflow = Workflow(
        name=FLOW_NAME,
        definition=workflow_definition,
        role=WORKFLOW_ROLE,
        execution_input=execution_input)
    workflow.create()

    # Workflow の実行
    execution = workflow.execute(inputs=inputs)
