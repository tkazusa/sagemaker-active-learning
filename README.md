# Amazon SageMaker を使った Active Learning の実装
## 能動学習実施までの流れ
- 下記の一連の流れを StepFunctions でパイプラインとして実施する。
    - 推論ジョブ：AWS Batch で推論を実施し、能動学習対象となるデータを選別する
    - ラベリングジョブ：AWS Lambda で SageMaker の `[CreateLabelingJob](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_labeling_job)` API でラベリングジョブを作成する

## 推論ジョブに必要なコンポーネント
AWS Batch を用いて推論を行う場合に必要なコンポーネントは下記。
- 推論用コンテナイメージ
- AWS Batch ジョブ(BatchJobDefinition、BatchJobName、BatchJobQueue)
- IAM ロール
    - AWS Batch用のロール：今回は `Job role` を指定しておりません。

## ラベリングジョブに必要なコンポーネント
AWS Lambda で  ラベリングジョブを作成する場合に必要なコンポーネントは下記。
- ラベリングジョブ作成用 Lambda 関数: [create_labeling_job.py](https://github.com/tkazusa/sagemaker-active-learning/blob/master/labeling/create_labeling_job.py)
- SageMaker Ground Truth HTML テンプレート: [segmentation.liquid.html](https://github.com/tkazusa/sagemaker-active-learning/blob/master/labeling/segmentation.liquid.html)
- SageMaker Ground Truth ラベル設定: [LabelCategoryconfig.json](https://github.com/tkazusa/sagemaker-active-learning/blob/master/labeling/LabelCategoryConfig.json)
- プレラベリング Lambda 関数：pretask.py
- ポストラベリング Lambda 関数：posttask.py
- IAM ロール
    - ラベリングジョブ作成用 Lambda 関数：
    - SageMaker ラベリングジョブ用のロール: AWSLambdaFullAccess と AmazonSageMakerFullAccess を付与
    - プレラベリング Lambda 関数用のロール: AWSLambdaBasicExecutionRole と、 AmazonS3ReadOnlyAccess
    - ポストラベリング　Lambda 関数用のロール: AWSLambdaBasicExecutionRole

## 能動学習パイプラインに必要なコンポーネント
AWS Step Functions で能動学習パイプラインを構築するために必要なコンポーネントは下記。
- 能動学習パイプライン：active_learning_pipeline.py
- 推論ジョブコンポーネント
- ラベリングジョブコンポーネント
- IAM ロール
    - 能動学習パイプライン：
    
## 準備の手順
- 必要なライブラリのインストール：requirments.txt
- 推論ジョブの準備
    - 推論用コンテナイメージを作成し Amazon ECR へ登録する：ecr-regist-batch.sh
    - AWS Batch ジョブを作成する
- ラベリングジョブの準備
    - ラベリングジョブのコンポーネントを作成する
        - HTMLテンプレート、プレラベリング Lambda、ポストラベリング Lambda、ワーカーチーム、ラベル設定
    - SageMaker の `CreateLabelingJob` API でラベリングジョブを作成するための Lambda 関数を作成する
- 能動学習用のパイプラインの作成


## TODO 
- 推論後に推論対象になるデータを選定するジョブの作成

## 参考
- [Amazon Augmented AI をヒューマンレビューに使用する](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/use-augmented-ai-a2i-human-review-loops.html)
- [カスタムタスクタイプで Amazon Augmented AI を使用する](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/a2i-task-types-custom.html)
- [Amazon Augmented AI Sample Notebooks](https://github.com/aws-samples/amazon-a2i-sample-jupyter-notebooks)
- [Bring your own model for Amazon SageMaker labeling workflows with active learning](https://aws.amazon.com/jp/blogs/machine-learning/bring-your-own-model-for-amazon-sagemaker-labeling-workflows-with-active-learning/)
