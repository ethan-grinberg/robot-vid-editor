from pathlib import Path
import os
import sys
from robot_vid_editor.process_audio import ProcessAudio
from robot_vid_editor.edit_video import EditVideo

def main(dir, title, audio):
    audio_file = "audio/" + audio + ".wav"
    audio = ProcessAudio(audio_file, os.path.join(dir, "models"))
    words = audio.extract_keywords()

    print('KEYWORDS:')
    print(words)

    video = EditVideo(words, "images/", title, audio_file)
    video.edit_video()

project_dir = Path(__file__).resolve().parents[0]
title = sys.argv[1]
audio = sys.argv[2]
main(project_dir, title, audio)