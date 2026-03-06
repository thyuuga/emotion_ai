# Emotion AI

一个基于 **MacBERT** 的中文情感分类项目，用于对句子进行情绪识别。

该项目实现了一个简单完整的 NLP 流程，包括：

- 数据集构建
- 数据集划分
- 模型训练
- 情绪推理

适合作为 **中文情感分类（Emotion Classification）** 的学习项目或基础框架。

---

## 项目功能

本项目实现了一个句子级情绪分类器，可以识别以下情绪：

- 开心
- 生气
- 难过
- 害羞
- 平常

示例：

> 输入：`今天真是太开心了！`
>
> 输出：`情绪：开心，置信度：0.94`

---

## 项目结构

```
emotion_ai
│
├── train_emotion.py          # 模型训练脚本
├── infer_emotion.py          # 情绪推理脚本
├── emotion_analyzer.py       # 情绪分析逻辑
├── labels.py                 # 情绪标签定义
│
├── emotion_dataset.jsonl     # 情绪数据集
├── split_dataset.py          # 数据集划分脚本
│
├── check_macbert.py          # MacBERT模型检查脚本
└── hfl_chinese-macbert-base.py  # MacBERT加载脚本
```

---

## 使用模型

本项目使用 HuggingFace 的中文预训练模型：

```
hfl/chinese-macbert-base
```

MacBERT 是 BERT 的改进版本，在中文 NLP 任务中表现较好。

---

## 安装依赖

建议使用 Python 3.9+。

```bash
pip install torch transformers datasets scikit-learn
```

---

## 训练模型

```bash
python train_emotion.py
```

训练完成后会生成模型文件。

> **注意：** 由于 GitHub 文件大小限制，模型权重未包含在仓库中。

---

## 情绪推理

```bash
python infer_emotion.py
```

示例代码：

```python
text = "今天心情很好"
result = analyze_emotion(text)
print(result)
```

输出示例：

```json
{
  "emotion": "开心",
  "confidence": 0.92
}
```

---

## 数据格式

数据集采用 JSONL 格式：

```jsonl
{"text": "今天很开心", "label": "开心"}
{"text": "有点难过", "label": "难过"}
```

每一行是一条训练数据。

---

## 未来改进

- 支持更多情绪类别
- 使用更大规模数据集
- 导出 ONNX 模型
- 构建 API 服务
- 与聊天机器人系统结合

---

## License

MIT License

---

# English Version

## Emotion AI

Emotion AI is a Chinese emotion classification project based on **MacBERT**.

It provides a simple NLP pipeline including:

- Dataset preparation
- Dataset splitting
- Model training
- Emotion inference

This project can serve as a learning example for Chinese emotion classification tasks.

### Features

The classifier can recognize several emotions including:

- Happy
- Angry
- Sad
- Shy
- Neutral

Example:

> Input: `今天真是太开心了！`
>
> Output: `Emotion: Happy, Confidence: 0.94`

### Project Structure

```
emotion_ai
│
├── train_emotion.py
├── infer_emotion.py
├── emotion_analyzer.py
├── labels.py
│
├── emotion_dataset.jsonl
├── split_dataset.py
│
├── check_macbert.py
└── hfl_chinese-macbert-base.py
```

### Model

This project uses a pretrained Chinese language model from HuggingFace:

```
hfl/chinese-macbert-base
```

MacBERT is an improved version of BERT and performs well on Chinese NLP tasks.

### Installation

Recommended: Python 3.9+

```bash
pip install torch transformers datasets scikit-learn
```

### Training

```bash
python train_emotion.py
```

The trained model will be generated locally.

> **Note:** Model weights are not included in this repository due to GitHub file size limits.

### Inference

```bash
python infer_emotion.py
```

Example:

```python
text = "今天心情很好"
result = analyze_emotion(text)
print(result)
```

Output:

```json
{
  "emotion": "happy",
  "confidence": 0.92
}
```

### Future Work

- Support more emotion classes
- Train on larger datasets
- Export ONNX models
- Build REST API service
- Integrate into chatbot systems
