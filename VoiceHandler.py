from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
from os import remove

"""
    @Creation data: 
    - 06/28/2020
    @Authors: 
    - Oste Jannick (Original interface (messy))
    - Gabriel Amara (Improved readabilty, Added comments) 
    @description:
        SpeechInterface provides two methods to respectively "convert" Audio <--> Text
        The instance of the class contains attribute to parameter how the conversion should be done
        listener : Recognizer object to handle Audio and Speech recognition
        phrase_time_limit : maximum number of seconds for the audio sample when listening
        speech_file_location : filepath of the temp ".mp3" file created to read out loud
"""


class SpeechInterface:
    def __init__(self, phrase_time_limit=5, speech_file_location="assets/speech.mp3"):
        self.listener: sr = sr.Recognizer()
        self.phrase_time_limit: float = phrase_time_limit
        self.speech_file_location: str = speech_file_location

    def listen(self) -> str:
        """
        This method listen to the user microphone and map the audio input to a corresponding text output
        :return: Text extracted from the user's record
        """

        print("Listening for audio input")

        with sr.Microphone() as microphone:
            parsed_audio = self.listener.listen(microphone, phrase_time_limit=self.phrase_time_limit)

        try:
            return self.listener.recognize_google(parsed_audio)
        except Exception as e:
            print("Unable to parse microphone audio")
            return ""

    def speak(self, text: str) -> None:
        """
        This method reads the given text out loud
        :param text: The text to read
        :return: None
        TODO ? may add some ``status: bool`` return value to handle possible errors (True -> ok, False -> error)
        """

        speech = gTTS(text=text, lang="en", slow=False)
        speech.save(self.speech_file_location)
        playsound(self.speech_file_location)
        remove(self.speech_file_location)
