import gtts
from playsound import playsound
import os


def play_sound(speech_text, file_name):

    if file_name in os.listdir(os.curdir):
        if ".mp3" in file_name:
            os.remove(file_name)

    tts = gtts.gTTS(speech_text, lang="en-au")
    tts.save(file_name)
    playsound(file_name)





if __name__ == "__main__":
    play_sound(speech_text="Hello", file_name="sound_file.mp3")
