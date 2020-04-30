### ①Augmented AI を使う
バッチ推論を行うタイミングで、それぞれの推論毎に confidence を確認。能動学習用のラベルジョブへデータを送る。推論エンドポイントに組み込むのに向いていると感じる。

[メリット]
- SageMaker GroundTruth のラベリングジョブを立ち上げる
- 一度 WorkFlow を定義するとあとから、推論データを追加して、能動学習を行うことができる

[デメリット]
- 能動学習後の出力がs3においてデータのパスのディレクトリがわかれた形で保存される

### ②SageMaker GroundTruth と Lambda、StepFunctions を使う
推論ジョブのどこかしらのタイミングで confidence を確認し、推論が終わったタイミングでLambdaにてconfidenceを確認、Lambdaにてラベリングジョブを立ち上げる。

![SageMakerでの能動学習](https://github.com/tkazusa/sagemaker-active-learning/blob/master/images/byom-sagemaker-1.gif?raw=true "サンプル")

[メリット]
- 通常のラベリングジョブと変わらずに使える

[デメリット]
- 後から推論データを追加する場合には、別途ラベリングジョブを立ち上げることになり煩雑 

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
                


