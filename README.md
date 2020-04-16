# SageMaker を使った Active Learning の実装
## 実装の方針
- Augmented AI を使う
- SageMaker GroundTruth と StepFunctions を使う


### Augmented AI を使う
1. カスタムワーカーテンプレートを作成する
    a. テンプレート名、IAMロール、テンプレートを設定
2. ヒューマンレビューワークフローを作成する
    a. Amazon A2I `CreateFlowDefinition` API を使用する
  

## 参考
- [Bring your own model for Amazon SageMaker labeling workflows with active learning](https://aws.amazon.com/jp/blogs/machine-learning/bring-your-own-model-for-amazon-sagemaker-labeling-workflows-with-active-learning/)
