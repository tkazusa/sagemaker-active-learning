# Amazon SageMaker を使った Active Learning の実装
## 実装の方針
### Augmented AI を使う
バッチ推論を行うタイミングで、それぞれの推論毎に confidence を確認。能動学習用のラベルジョブへデータを送る。
[メリット]
- SageMaker GroundTruth のラベリングジョブを立ち上げる
- 一度 WorkFlow を定義するとあとから、推論データを追加して、能動学習を行うことができる
[デメリット]
- 能動学習後の出力がs3においてデータのパスのディレクトリがわかれた形で保存される

### SageMaker GroundTruth と Lambda、StepFunctions を使う
推論ジョブのどこかしらのタイミングで confidence を確認し、推論が終わったタイミングでLambdaにてconfidenceを確認、Lambdaにてラベリングジョブを立ち上げる。

[メリット]
- 通常のラベリングジョブと変わらずに使える
[デメリット]
- 

### Augmented AI を使う
1. カスタムワーカーテンプレートを作成する
    - テンプレート名、IAMロール、テンプレートを設定
2. ヒューマンレビューワークフローを作成する
    - Amazon A2I `CreateFlowDefinition` API を使用する
        1. FlowDefinition を作成する
            - フローの定義名、IAMロールを設定
            - HumanLoopConfigの設定
                - だれがやるのか：ワークスチーム ARN(SageMaker Ground Truth の)
                - どのタスクやるのか：ヒューマンタスク(作成したカスタムワーカーテンプレ、UI)の ARN
                - タスク数、タイトル、説明を記載
         2. ヒューマンループ を開始する
            -  [StartupHumanLoop](https://docs.aws.amazon.com/augmented-ai/2019-11-07/APIReference/API_StartHumanLoop.html) を開始する
                - DataAttributes: 顧客によって指定された data attribute
                - FlowDefinitionArn: FlowDefinition の ARN
                - HumanLoopInput: Serialized input from the human loop.
                - HumanLoopName: ヒューマンループの名前を入れる 
                
                
  

## 参考
- [Amazon Augmented AI をヒューマンレビューに使用する](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/use-augmented-ai-a2i-human-review-loops.html)
- [カスタムタスクタイプで Amazon Augmented AI を使用する](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/a2i-task-types-custom.html)
- [Amazon Augmented AI Sample Notebooks](https://github.com/aws-samples/amazon-a2i-sample-jupyter-notebooks)
- [Bring your own model for Amazon SageMaker labeling workflows with active learning](https://aws.amazon.com/jp/blogs/machine-learning/bring-your-own-model-for-amazon-sagemaker-labeling-workflows-with-active-learning/)

