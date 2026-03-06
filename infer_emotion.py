import torch
import json
import sys
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = "emotion_model"

# 推理阈值
CONF_HIGH = 0.60
CONF_LOW = 0.45

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)

model.eval()


def predict(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=64
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]

    id2label = model.config.id2label

    results = []
    for i, p in enumerate(probs):
        label = id2label.get(i, id2label.get(str(i)))
        results.append({
            "emotion": label,
            "prob": float(p)
        })

    # 按概率排序
    results = sorted(results, key=lambda x: x["prob"], reverse=True)

    top = results[0]

    # 阈值策略
    if top["prob"] >= CONF_HIGH:
        final_emotion = top["emotion"]
    elif top["prob"] >= CONF_LOW:
        final_emotion = top["emotion"]
    else:
        final_emotion = "平常"

    return {
        "text": text,
        "emotion": final_emotion,
        "confidence": round(top["prob"], 3),
        "candidates": results
    }


def main():
    print("Emotion classifier ready. 输入一句话测试 (exit退出)")
    while True:
        text = input("\nTEXT: ").strip()

        if text.lower() in ["exit", "quit"]:
            break

        result = predict(text)

        print("\nRESULT:")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()