from transformers import pipeline

lyrics_model = pipeline(
    "text-generation",
<<<<<<< HEAD
    model="distilgpt2",
    tokenizer="distilgpt2"
=======
    model="models/lyrics-gpt2-trained",
    tokenizer="models/lyrics-gpt2-trained"
>>>>>>> origin
)