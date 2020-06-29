import random

from CommandHandler import CommandHandler
from VoiceHandler import VoiceHandler
import difflib, requests, bs4


class Main:
    def __init__(self):
        self.voice = VoiceHandler()
        self.command_handler = CommandHandler()
        self.commands = [k for k in list(self.command_handler.__class__.__dict__.keys()) if "__" not in k]
        self.listen_for_commands()

    def listen_for_commands(self):
        assistend_spoken = False

        while True:
            if not assistend_spoken:
                self.voice.textToSpeech("Waiting for your command sir...")
                assistend_spoken = True

            text: str = self.voice.listenForSpeech()
            if text:
                listed_text = [text] if not " " in text else text.split()
                parsed_command = None
                parsed_arguments = None
                # parse correct commands/arguments
                if listed_text[0] in self.commands:
                    parsed_command = listed_text[0]
                    if len(listed_text) > 1:
                        parsed_arguments = listed_text[1:]
                elif len(listed_text) > 1 and "_".join(listed_text[:2]).lower() in self.commands:
                    parsed_command = "_".join(listed_text[:2]).lower()
                    if len(listed_text) > 2:
                        parsed_arguments = listed_text[2:]
                elif "_".join(listed_text) in self.commands:
                    parsed_command = "_".join(listed_text)
                else:
                    # Search a command with more as 75% similarity
                    for command in self.commands:
                        # compare text to each command and calculate the similairity between the strings
                        sequence = difflib.SequenceMatcher(isjunk=None, a=text, b=command)
                        diffrence = round(sequence.ratio() * 100, 1)  # *100 due being stored in fractions.
                        if diffrence >= 75:
                            parsed_command = command
                            break

                if parsed_command: # if command was valid, run with(out) arguments
                    if parsed_command != "commands":
                        self.voice.textToSpeech("Command %s has been found, executing command" % parsed_command.replace("_", " "))

                    command = getattr(self.command_handler, parsed_command)

                    if not parsed_arguments:
                        command()
                    else:
                        command(parsed_arguments)

                    assistend_spoken = False
                else:
                    print(text)
                    self.voice.textToSpeech("Could not find the command %s" % text)


if __name__ == "__main__":
    Main()