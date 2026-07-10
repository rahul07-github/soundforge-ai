"""
vocal_generator.py — TTS only, male voice, partial pitch-shaping.
"""

import os, uuid, asyncio, edge_tts
import numpy as np, librosa, soundfile as sf
from pydub import AudioSegment

VOCALS_DIR = "backend/app/storage/generated/vocals"
os.makedirs(VOCALS_DIR, exist_ok=True)

VOICES = {
    "male": "en-US-GuyNeural",
    "male_deep": "en-US-ChristopherNeural",
    "male_warm": "en-US-EricNeural",
    "female": "en-US-JennyNeural",
}
DEFAULT_VOICE = VOICES["male"]


async def _tts_generate(text, output_path, voice):
    await edge_tts.Communicate(text, voice).save(output_path)
    return output_path


def apply_sing_effect(input_path, output_path, semitone_variation=1.5):
    y, sr = librosa.load(input_path, sr=None, mono=True)
    n_steps = np.sin(np.linspace(0, 3 * np.pi, num=10)) * semitone_variation
    seg_len = len(y) // len(n_steps)
    out = []
    for i, shift in enumerate(n_steps):
        start = i * seg_len
        end = start + seg_len if i < len(n_steps) - 1 else len(y)
        seg = y[start:end]
        if len(seg):
            out.append(librosa.effects.pitch_shift(seg, sr=sr, n_steps=shift))
    y_out = np.concatenate(out)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, y_out, sr)
    AudioSegment.from_file(output_path).export(output_path, format="mp3", bitrate="192k")
    return output_path


def generate_vocal(lyrics, voice=DEFAULT_VOICE, apply_effect=True):
    file_id = str(uuid.uuid4())[:8]
    raw_path = os.path.join(VOCALS_DIR, f"{file_id}_raw.mp3")
    asyncio.run(_tts_generate(lyrics, raw_path, voice))
    if not apply_effect:
        return raw_path
    final_path = os.path.join(VOCALS_DIR, f"{file_id}_vocal.mp3")
    return apply_sing_effect(raw_path, final_path)


if __name__ == "__main__":
    generate_vocal("Sunlight breaks through a heavy gray sky", voice=VOICES["male"])