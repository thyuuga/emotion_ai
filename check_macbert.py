from transformers import AutoTokenizer, AutoModel

MODEL_NAME = "hfl/chinese-macbert-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

print("✅ model loaded:", MODEL_NAME)
print("✅ vocab size:", tokenizer.vocab_size)
print("✅ hidden size:", model.config.hidden_size)