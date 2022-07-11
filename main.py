from pathlib import Path
import os
import sys
from robot_vid_editor.process_audio import ProcessAudio
from robot_vid_editor.edit_video import EditVideo
from robot_vid_editor.__init__ import create_app

def main(dir, title, audio):
    audio_file = "audio/" + audio + ".wav"
    audio = ProcessAudio(audio_file, os.path.join(dir, "models"))
    words = audio.extract_keywords()

    print('KEYWORDS:')
    print(words)

    video = EditVideo(words, "images/", title, audio_file)
    video.edit_video()

def flask():
    app = create_app()
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == '__main__':
    project_dir = Path(__file__).resolve().parents[0]
    if len(sys.argv) > 1:
        title = sys.argv[1]
        audio = sys.argv[2]
        main(project_dir, title, audio)
    else:
        flask()