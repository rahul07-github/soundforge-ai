from transformers import pipeline

lyrics_model = pipeline(
    "text-generation",
    model="distilgpt2"
)