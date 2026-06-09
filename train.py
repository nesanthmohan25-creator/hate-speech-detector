import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("data/train.csv")

# ETHOS dataset format
df = df[["Data", "Response"]]
df.columns = ["text", "label"]

# Reduce size to avoid freezing
df = df.sample(n=800, random_state=42)

print("Dataset size:", df.shape)

# -----------------------
# SPLIT
# -----------------------
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["text"], df["label"], test_size=0.1, random_state=42
)

# -----------------------
# TOKENIZER
# -----------------------
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

train_encodings = tokenizer(
    list(train_texts),
    truncation=True,
    padding=True,
    max_length=64
)

val_encodings = tokenizer(
    list(val_texts),
    truncation=True,
    padding=True,
    max_length=64
)

# -----------------------
# DATASET CLASS
# -----------------------
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = list(labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = CustomDataset(train_encodings, train_labels)
val_dataset = CustomDataset(val_encodings, val_labels)

# -----------------------
# MODEL
# -----------------------
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

# -----------------------
# TRAINING ARGS (NO evaluation_strategy HERE)
# -----------------------
training_args = TrainingArguments(
    output_dir="./model",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    logging_steps=50
)

# -----------------------
# TRAINER
# -----------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# -----------------------
# TRAIN
# -----------------------
print("🚀 Training started...")
trainer.train()

# -----------------------
# SAVE
# -----------------------
model.save_pretrained("./model")
tokenizer.save_pretrained("./model")

print("✅ Training complete!")
