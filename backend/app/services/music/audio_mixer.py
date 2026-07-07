from pathlib import Path
from pydub import AudioSegment

AudioSegment.converter = r"E:\ffmpeg2\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"E:\ffmpeg2\bin\ffprobe.exe"

def mix_audio(vocal_path: str, beat_path: str, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    vocal = AudioSegment.from_file(vocal_path) + 2
    beat = AudioSegment.from_file(beat_path) + 4

    while len(beat) < len(vocal):
        beat += beat

    beat = beat[:len(vocal)]

    final = beat.overlay(vocal)
    final = final[:20000]

    final.export(output_path, format="mp3")
    return output_path