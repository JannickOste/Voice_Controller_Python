import os, random, pyautogui, time, httplib2, requests

from VoiceHandler import VoiceHandler
import pygetwindow

class CommandHandler:
    def __init__(self):
        self.voiceh = VoiceHandler()

    def commands(self):
        self.voiceh.textToSpeech("Voice commands are: ")
        for i in [k for k in list(self.__class__.__dict__.keys()) if "__" not in k]:
            i = i if not "_" in i else i.replace("_", " ")
            self.voiceh.textToSpeech(i)
            print("- %s" % i)

    """ Software shortcuts """
    def open_firefox(self, *args, **kwargs):
        print("Opening firefox")
        os.chdir("C:\\Program Files\\Mozilla Firefox")

        if not args:
            os.system("firefox.exe")
        else:
            parsed_url = None
            for i in ["be", "com", "nl", "org", "co"]:
                current_url = "http://www.%s.%s" % ("".join(args[0]).lower(), i)
                try:
                    header = httplib2.Http()
                    response = header.request(current_url, "HEAD")
                    if int(response[0]["status"]) < 400:
                        parsed_url = current_url
                except Exception:
                    continue
                finally:
                    if parsed_url:
                        break
            if parsed_url:
                os.system("firefox.exe %s" % parsed_url)
            else:
                self.voiceh.textToSpeech("Unable to find correct url.")

    def play_music(self, play=True):
        self.stop_music()
        os.system("spotify.exe")
        time.sleep(5)
        if play:
            play_location = pyautogui.locateOnScreen("assets/images/spotify_play.png", confidence=.9)
            if play_location:
                pyautogui.click(int(play_location.left+(play_location.width/2)),
                                int(play_location.top+(play_location.height/2)))

    def next_song(self):
        window = pygetwindow.getWindowsWithTitle("spotify")
        if window:
            window[0].activate()
            next_loc = pyautogui.locateOnScreen("assets/images/next_song.png", confidence=.9)
            if next_loc:
                pyautogui.click(int(next_loc.left+(next_loc.width/2)),
                                int(next_loc.top+(next_loc.height/2)))

    def previous_song(self):
        window = pygetwindow.getWindowsWithTitle("spotify")
        if window:
            window[0].activate()
            prev_loc = pyautogui.locateOnScreen("assets/images/previous_song.png", confidence=.9)
            if prev_loc:
                pyautogui.click(int(prev_loc.left+(prev_loc.width/2)),
                                int(prev_loc.top+(prev_loc.height/2)))

    def stop_music(self): os.system("taskkill /f /im spotify.exe")

    def open_partitions(self): os.system("diskmgmt.msc")

    def open_notepad(self): os.system("notepad.exe")

    def open_calculator(self): os.system("calc")

    def open_terminal(self): os.system("start cmd.exe")

    """ Power control """
    def sleep(self): os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def shutdown(self): os.system("shutdown.exe -s -t 0")

    def restart(self): os.system("shutdown -r -t 5")

    def tell_me_a_joke(self):
        print("Telling a joke")
        # Fetch jokes from API
        url = "https://official-joke-api.appspot.com/random_ten"
        url_response = eval(requests.get(url).text)
        random_joke = random.choice(url_response)
        self.voiceh.textToSpeech(random_joke["setup"])
        self.voiceh.textToSpeech(random_joke["punchline"])


if __name__ == "__main__":
    print("CommandHandler isnt an executable class, run program from Main.py")
    exit(0)