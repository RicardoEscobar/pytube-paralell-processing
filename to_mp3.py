"""This converts a webm file to mp3."""
from pathlib import Path
from pydub import AudioSegment

def to_mp3(path: Path = Path()):
    try:
        # load the webm audio file
        audio_file = AudioSegment.from_file(path, format="webm")

        # export the audio to mp3 format
        out_path = path.with_suffix('.mp3')

        audio_file.export(out_path, format="mp3")

        # delete the webm file
        path.unlink()
    except Exception as e:
        print(f"Exception: {type(e).__name__}\nMessage: {e}\nPath: {path}")

if __name__ == '__main__':
    to_mp3(Path('Música - PLZOGNlgi8GGncx1etrSzhrHM1GqoFindD\\SIGMA SONG Mareux - The Perfect Girl  EPIC GIGACHAD VERSION (American Psycho).webm'))