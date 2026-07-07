import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)

DATASET_PATH = "datasets/lyrics/Songs.csv"
BASE_MODEL = "distilgpt2"
OUTPUT_DIR = "models/lyrics-gpt2"


df = pd.read_csv(DATASET_PATH)

df = df.dropna(subset=["Lyrics"])
df = df.drop_duplicates(subset=["Lyrics"])

texts = []

for _, row in df.iterrows():
    artist = row.get("Artist", "")
    title = row.get("Title", "")
    lyrics = row.get("Lyrics", "")

    text = f"""
Artist: {artist}
Title: {title}

Lyrics:
{lyrics}
"""
    texts.append(text)

dataset = Dataset.from_dict({
    "text": texts
})

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)


def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=256
    )


tokenized_dataset = dataset.map(
    tokenize,
    batched=True,
    remove_columns=["text"]
)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=1,
    save_steps=500,
    save_total_limit=2,
    logging_steps=50,
    prediction_loss_only=True
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)

trainer.train()

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Lyrics model trained and saved successfully.")