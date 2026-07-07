from pathlib import Path
from pydub import AudioSegment

AudioSegment.converter = r"E:\ffmpeg2\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"E:\ffmpeg2\bin\ffprobe.exe"


def mix_audio(vocal_path: str, beat_path: str, output_path: str):

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    vocal = AudioSegment.from_mp3(vocal_path)
    beat = AudioSegment.from_mp3(beat_path)

    # Increase beat volume
    beat -= 4

    # Reduce vocal volume slightly
    vocal += 8

    # Extend beat if shorter
    while len(beat) < len(vocal):
        beat += beat

    beat = beat[:len(vocal)]

    final = beat.overlay(vocal)

    # Limit demo to 20 seconds
    final = final[:20000]

    final.export(output_path, format="mp3")

    return output_path