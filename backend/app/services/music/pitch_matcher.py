from pydub import AudioSegment
from pathlib import Path

AudioSegment.converter = r"D:\ffmpeg2\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"D:\ffmpeg2\bin\ffprobe.exe"


def match_vocal_to_beat(vocal_path: str, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    import os

    print("=" * 50)
    print("Vocal Path :", vocal_path)
    print("File Exists:", os.path.exists(vocal_path))
    print("=" * 50)

    vocal = AudioSegment.from_file(vocal_path)

    # make voice slightly faster and higher
    new_frame_rate = int(vocal.frame_rate * 1.08)

    changed = vocal._spawn(
        vocal.raw_data,
        overrides={"frame_rate": new_frame_rate}
    )

    changed = changed.set_frame_rate(vocal.frame_rate)

    changed.export(output_path, format="mp3")

    return output_path