import json
import uuid
import boto3

id = uuid.uuid4().hex


LabelingJobName='active-learning-labeling-{}'.format(id)
LabelAttributeName='active-learning-labeling'

S3OutputPath='S3 PATH'
RoleArn='ROLE ARN'
LabelCategoryConfigS3Uri='S3 PATH'

ManifestS3Uri='S3 PATH'
InputConfig = {'DataSource': {'S3DataSource': {'ManifestS3Uri': ManifestS3Uri}}}
OutputConfig = {'S3OutputPath': S3OutputPath}


## HumanTaskConfigの設定
WorkteamArn='WORK TEAM ARN'
UiTemplateS3Uri='S3 PATH'
PreHumanTaskLambdaArn='LAMBDA ARN'
TaskTitle='active-learning-labeling-job'
TaskDescription='labeling task for active learning from lambda'
AnnotationConsolidationLambdaArn='LAMBDA ARN'

HumanTaskConfig={
    'WorkteamArn': WorkteamArn,
    'UiConfig': {'UiTemplateS3Uri': UiTemplateS3Uri},
    'PreHumanTaskLambdaArn': PreHumanTaskLambdaArn,
    'TaskTitle': TaskTitle,
    'TaskDescription': TaskDescription,
    'NumberOfHumanWorkersPerDataObject': 1,
    'TaskTimeLimitInSeconds': 120,
    'AnnotationConsolidationConfig': {'AnnotationConsolidationLambdaArn': AnnotationConsolidationLambdaArn}, 
}


def lambda_handler(event, context):
    """Ground Truth のラベリングジョブを作成
    """
    client = boto3.client('sagemaker')
    response = client.create_labeling_job(
        LabelingJobName=LabelingJobName,
        LabelAttributeName=LabelAttributeName,
        InputConfig=InputConfig,
        OutputConfig=OutputConfig,
        RoleArn=RoleArn,
        LabelCategoryConfigS3Uri=LabelCategoryConfigS3Uri,
        HumanTaskConfig=HumanTaskConfig)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Labeling job created')
    }