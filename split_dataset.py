import json
import random
from collections import defaultdict

random.seed(42)

INPUT_PATH = "emotion_dataset.jsonl"
TRAIN_PATH = "data/train.jsonl"
DEV_PATH = "data/dev.jsonl"

groups = defaultdict(list)

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        groups[item["label"]].append(line)

train_lines = []
dev_lines = []

for label, lines in groups.items():
    random.shuffle(lines)
    split = int(len(lines) * 0.8)
    train_lines.extend(lines[:split])
    dev_lines.extend(lines[split:])

random.shuffle(train_lines)
random.shuffle(dev_lines)

with open(TRAIN_PATH, "w", encoding="utf-8") as f:
    for line in train_lines:
        f.write(line + "\n")

with open(DEV_PATH, "w", encoding="utf-8") as f:
    for line in dev_lines:
        f.write(line + "\n")

print(f"train: {len(train_lines)}")
print(f"dev: {len(dev_lines)}")