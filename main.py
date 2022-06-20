from pathlib import Path
import os
import sys
from src.process_audio import ProcessAudio
from src.edit_video import EditVideo

def main(dir):
    audio = ProcessAudio("data/test.wav", os.path.join(dir, "models"))
    words = audio.extract_keywords()

    video = EditVideo(words, "images/")

if __name__ == '__main__':
    project_dir = Path(__file__).resolve().parents[0]
    main(project_dir)