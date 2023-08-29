---
license: apache-2.0
tags:
- generated_from_trainer
datasets:
- glue
metrics:
- accuracy
model-index:
- name: distilbert-base-uncased-finetuned-sst2
  results:
  - task:
      name: Text Classification
      type: text-classification
    dataset:
      name: glue
      type: glue
      config: sst2
      split: validation
      args: sst2
    metrics:
    - name: Accuracy
      type: accuracy
      value: 0.9025229357798165
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# distilbert-base-uncased-finetuned-sst2

This model is a fine-tuned version of [distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased) on the glue dataset.
It achieves the following results on the evaluation set:
- Loss: 0.2805
- Accuracy: 0.9025

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 512
- eval_batch_size: 512
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 5

### Training results

| Training Loss | Epoch | Step | Validation Loss | Accuracy |
|:-------------:|:-----:|:----:|:---------------:|:--------:|
| No log        | 1.0   | 132  | 0.2592          | 0.8888   |
| No log        | 2.0   | 264  | 0.2770          | 0.8979   |
| No log        | 3.0   | 396  | 0.2805          | 0.9025   |
| 0.1914        | 4.0   | 528  | 0.2975          | 0.9014   |
| 0.1914        | 5.0   | 660  | 0.3026          | 0.9002   |


### Framework versions

- Transformers 4.29.1
- Pytorch 2.0.1+cu117
- Datasets 2.12.0
- Tokenizers 0.13.3
