<<<<<<< HEAD
def build_prompt(user_prompt):

    return f"""
You are a professional songwriter.

Write ONLY song lyrics.

Rules:
- Do not write stories.
- Do not write websites.
- Do not write URLs.
- Do not mention books.
- Do not explain anything.
- Output only lyrics.

Structure:

[Verse 1]

[Chorus]

[Verse 2]

[Bridge]

Prompt:
{user_prompt}
=======
def build_prompt(
    user_prompt,
    genre="Pop",
    mood="Uplifting",
    theme=None,
    tempo=120,
    key="C Major",
    vocal_type="Male Lead",
    language="English",
    instruments="acoustic guitar, soft drums",
):
    """
    Must match the EXACT format used in train_lyrics_model.py's training_text,
    or the fine-tuned model won't recognize the prompt pattern at all.
    """
    theme = theme or user_prompt

    return f"""User Prompt: {user_prompt}
Genre: {genre}
Mood: {mood}
Theme: {theme}
Tempo: {tempo}
Key: {key}
Vocal Type: {vocal_type}
Language: {language}
Instruments: {instruments}
>>>>>>> origin

Lyrics:
"""