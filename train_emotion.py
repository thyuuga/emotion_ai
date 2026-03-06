import json
import numpy as np
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from sklearn.metrics import accuracy_score, f1_score

from labels import label2id, id2label

MODEL_NAME = "hfl/chinese-macbert-base"


def load_jsonl(path):
    texts = []
    labels = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            texts.append(item["text"])
            labels.append(label2id[item["label"]])
    return Dataset.from_dict({
        "text": texts,
        "label": labels
    })


train_dataset = load_jsonl("data/train.jsonl")
dev_dataset = load_jsonl("data/dev.jsonl")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=64
    )


train_dataset = train_dataset.map(tokenize)
dev_dataset = dev_dataset.map(tokenize)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)

    acc = accuracy_score(labels, preds)
    f1_macro = f1_score(labels, preds, average="macro")

    return {
        "accuracy": acc,
        "f1_macro": f1_macro
    }


model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

training_args = TrainingArguments(
    output_dir="emotion_model",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    num_train_epochs=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_ratio=0.1,
    logging_steps=10,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="eval_f1_macro",
    greater_is_better=True,
    save_total_limit=2,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset,
    processing_class=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

trainer.save_model("emotion_model")
tokenizer.save_pretrained("emotion_model")

print("训练完成 ✅")