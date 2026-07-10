import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)

DATASET_PATH = "datasets/lyrics/lyrics_to_music_dataset_large.csv"
BASE_MODEL = "distilgpt2"
OUTPUT_DIR = "models/lyrics-gpt2-trained"

df = pd.read_csv(DATASET_PATH)
df = df.dropna(subset=["prompt", "lyrics"])
df = df.drop_duplicates(subset=["lyrics"])

texts = []

for _, row in df.iterrows():
    prompt = row.get("prompt", "")
    genre = row.get("genre", "")
    mood = row.get("mood", "")
    theme = row.get("theme", "")
    tempo = row.get("tempo_bpm", "")
    key = row.get("musical_key", "")
    vocal_type = row.get("vocal_type", "")
    language = row.get("language", "")
    instruments = row.get("instrumental_tags", "")
    lyrics = row.get("lyrics", "")

    training_text = f"""
User Prompt: {prompt}
Genre: {genre}
Mood: {mood}
Theme: {theme}
Tempo: {tempo}
Key: {key}
Vocal Type: {vocal_type}
Language: {language}
Instruments: {instruments}

Lyrics:
{lyrics}
"""
    texts.append(training_text)

dataset = Dataset.from_dict({"text": texts})

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

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    num_train_epochs=2,
    per_device_train_batch_size=1,
    save_steps=500,
    save_total_limit=2,
    logging_steps=50
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

print("Training complete. Model saved at:", OUTPUT_DIR)