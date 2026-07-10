from transformers import pipeline

lyrics_model = pipeline(
    "text-generation",
    model="models/lyrics-gpt2-trained",
    tokenizer="models/lyrics-gpt2-trained"
)