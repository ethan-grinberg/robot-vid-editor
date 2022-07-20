import audioop
import wave
import json
from rake_nltk import Rake

from vosk import Model, KaldiRecognizer, SetLogLevel


class ProcessAudio:
    FRAME_RATE = 4000
    def __init__(self, audio_file, model_path):
        self.model = Model(model_path)

        # working with file names
        split_file = audio_file.split("/")
        self.file_pre = "/".join(split_file[:-1])
        self.file_suf = split_file[-1]
        # file names
        self.inFileName = audio_file
        self.outFileName = self.file_pre + "/mono-" + self.file_suf
    
    def extract_keywords(self):
        words = self.read_audio()

        print("ALL WORDS:")
        print(words)

        text = ""
        for word in words:
            text += word
            text += " "

        r = Rake()
        r.extract_keywords_from_text(text)
        keywords = r.get_ranked_phrases()

        keyword_dict = {}
        for keyword in keywords:
            all_words = keyword.split(" ")

            ts = words[all_words[0]]
            keyword_dict[keyword] = ts

        return keyword_dict
    
    def read_audio(self):
        self.__convert_single_channel()


        wf = wave.open(self.outFileName, "rb")
        rec = KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)

        results = []
        # recognize speech using vosk model
        while True:
            data = wf.readframes(self.FRAME_RATE)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result)
            
        part_result = json.loads(rec.FinalResult())
        results.append(part_result)

        wf.close()
        text = [word for word in results if len(word) != 1]
        text = text[0]['result']
        words = {word['word']: word['start'] for word in text}
        return words

    
    def __convert_single_channel(self):
        try:
            # open the input and output files
            inFile = wave.open(self.inFileName,'rb')
            outFile = wave.open(self.outFileName,'wb')
            # force mono
            outFile.setnchannels(1)
            # set output file like the input file
            outFile.setsampwidth(inFile.getsampwidth())
            outFile.setframerate(inFile.getframerate())
            # read
            soundBytes = inFile.readframes(inFile.getnframes())
            # convert to mono and write file
            monoSoundBytes = audioop.tomono(soundBytes, inFile.getsampwidth(), 1, 1)
            outFile.writeframes(monoSoundBytes)
            
        except Exception as e:
            print(e)
            
        finally:
            inFile.close()
            outFile.close()


       

    
