"""This converts a webm file to mp3."""
from pathlib import Path
from pydub import AudioSegment

def to_mp3(input_path: str = None, output_path: str = None) -> str:
    """This converts a webm file to mp3.
    args:
        input_path: Path to the webm file.
    returns:
        Path to the mp3 file."""
    
    # if no input path is given, use the current directory
    # else use the given path
    if input_path is None:
        input_path = Path()
    else:
        input_path = Path(input_path)

    # if no output path is given, use the same directory as the input path
    if output_path is None:
        output_path = input_path.parent
    else:
        output_path = Path(output_path)

    try:
        # load the webm audio file
        audio_file = AudioSegment.from_file(input_path, format="webm")

        # export the audio to mp3 format
        out_path = input_path.with_suffix('.mp3')
        output_path = output_path / out_path.name

        audio_file.export(output_path, format="mp3")
    except Exception as e:
        print(f"Exception: {type(e).__name__}\nMessage: {e}\nPath: {input_path}")
    else:
        # delete the webm file
        print(f"Converted {input_path} to {out_path}")
        input_path.unlink()

if __name__ == '__main__':
    to_mp3(Path('Música - PLZOGNlgi8GGncx1etrSzhrHM1GqoFindD\\SIGMA SONG Mareux - The Perfect Girl  EPIC GIGACHAD VERSION (American Psycho).webm'))