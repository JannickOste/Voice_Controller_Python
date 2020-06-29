from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
from os import remove


class VoiceHandler:
    # Listen for microphone audio.
    def listenForSpeech(self) -> str:
        listener: sr = sr.Recognizer()
        parsed_audio = ""

        print("Listening for audio input")
        with sr.Microphone() as microphone:
            parsed_audio = listener.listen(microphone, phrase_time_limit=5)

        try:
            text: str = listener.recognize_google(parsed_audio)
            return text
        except Exception as e:
            print("Unable to parse micrphone audio")
            return ""

    # Text to speech
    def textToSpeech(self, text_output: str) -> None:
        speech_file_location = "assets/speech.mp3"
        speech = gTTS(text=text_output, lang="en", slow=False)
        speech.save(speech_file_location)
        playsound(speech_file_location)
        remove(speech_file_location)


if __name__ == "__main__":
    print("VoiceHandler isnt an executable class, run program from Main.py")
    exit(0)