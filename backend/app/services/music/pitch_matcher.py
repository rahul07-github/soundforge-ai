from pydub import AudioSegment
from pathlib import Path

AudioSegment.converter = r"E:\ffmpeg2\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"E:\ffmpeg2\bin\ffprobe.exe"


def match_vocal_to_beat(vocal_path: str, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

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