from CommandHandler import CommandHandler


class Main:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.commands = [k for k in list(self.command_handler.__class__.__dict__.keys()) if "__" not in k]
        self.listen_for_commands()

    def listen_for_commands(self):
        assistend_spoken = False

        while True:
            if not assistend_spoken:
                self.command_handler.voiceh.speak("Waiting for your command sir...")
                assistend_spoken = True

            text: str = self.command_handler.voiceh.listen()
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
                    # Search for a command with 75% similarity
                    search = self.command_handler.misc.stringset_comparer(text, self.commands)
                    if search:
                        parsed_command = search

                if parsed_command: # if command was valid, run with(out) arguments
                    if parsed_command != "commands":
                        self.command_handler.voiceh.speak("Command %s has been found, executing command" % parsed_command.replace("_", " "))

                    command = getattr(self.command_handler, parsed_command)

                    if not parsed_arguments:
                        command()
                    else:
                        command(parsed_arguments)

                    assistend_spoken = False
                else:
                    print(text)
                    self.command_handler.voiceh.speak("Could not find the command %s" % text)


if __name__ == "__main__":
    Main()