import difflib, os
import pyautogui
import pygetwindow


class Misc:
    def __init__(self):
        pass

    def stringset_comparer(self, search_str, search_set, tresshold=75):
        # Search a command with more as 75% similarity
        for command in search_set:
            # compare text to each command and calculate the similairity between the strings
            sequence = difflib.SequenceMatcher(isjunk=None, a=search_str, b=command)
            diffrence = round(sequence.ratio() * 100, 1)  # *100 due being stored in fractions.
            if diffrence >= 75:
                return command

    def open_program(self, executable, directory=None):
        if directory:
            os.chdir(directory)

        os.system(executable)

    def search_screen(self, image, click_center=False):
        search_location = pyautogui.locateOnScreen(image)
        if search_location and click_center:
            pyautogui.click(int(search_location.left + (search_location.width / 2)),
                            int(search_location.top + (search_location.height / 2)))
        else:
            return search_location

    def focus_window(self, window_name: str):
        window = pygetwindow.getWindowsWithTitle(window_name)
        if window:
            window[0].activate()

    def window_exists(self, window_name: str): return True if len(pygetwindow.getWindowsWithTitle(window_name)) else False
