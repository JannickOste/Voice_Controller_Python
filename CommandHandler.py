import bs4, random, time, httplib2, requests, spotipy
from spotipy import SpotifyClientCredentials

from Misc import Misc
from VoiceHandler import SpeechInterface


class CommandHandler:
    def __init__(self):
        self.voiceh = SpeechInterface()
        self.misc = Misc()

    """ Software shortcuts """
    def open_firefox(self, *args, **kwargs):
        firefox_root = "C:\\Program Files\\Mozilla Firefox"
        # If no sub url specified, just open firefox
        if not args:
            self.misc.open_program(directory=firefox_root, executable="firefox.exe")
        else:
            # Otherwise attempt a search on multiple domain extension, if a site without 400+ error is found set as url
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

            # Open firefox with parsed url if a valid site has been found
            self.misc.open_program(directory=firefox_root, executable="firefox.exe %s" % parsed_url) if parsed_url else\
                self.voiceh.speak("Unable to find correct url.")

    def open_partitions(self): self.misc.open_program("diskmgmt.msc")

    def open_notepad(self): self.misc.open_program("notepad.exe")

    def open_calculator(self): self.misc.open_program("calc")

    def open_terminal(self): self.misc.open_program("start cmd.exe")

    """ Power control """
    def sleep(self): self.misc.open_program("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    def shutdown(self): self.misc.open_program("shutdown.exe -s -t 0")

    def restart(self): self.misc.open_program("shutdown -r -t 5")

    """ Software Control """
    def play_music(self, play=True):
        if self.misc.window_exists("spotify"):
            self.misc.focus_window("spotify")
        else:
            self.misc.open_program(executable="spotify.exe")

        time.sleep(5)
        if play:
            self.misc.search_screen(image="assets/images/spotify_play.png", click_center=True)


    def next_song(self):
        if self.misc.window_exists("spotify"):
            self.misc.focus_window("spotify")
        else:
            self.play_music(play=False)

        time.sleep(1)
        self.misc.search_screen(image="assets/images/next_song.png", click_center=True)

    def previous_song(self):
        if self.misc.window_exists("spotify"):
            self.misc.focus_window("spotify")
        else:
            self.play_music(play=False)

        time.sleep(1)
        self.misc.search_screen(image="assets/images/previous_song.png", click_center=True)

    def stop_music(self): self.misc.open_program("taskkill /f /im spotify.exe")

    def play_song(self, *args, **kwargs):
        client_id = ""
        client_secret = ""

        # Connecting to the api
        def connect_to_spotify():
            client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
            sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)
            return sp

        # Searching track based on search query.
        def search_track(search_query: str):
            conn = connect_to_spotify()
            result = conn.search(search_query, type="track")
            found_songs = {}
            for set in result["tracks"]["items"]:
                found_songs[set["name"].lower()] = set["uri"]
            return found_songs

        # If a valid client id & secret has been set attempt to scrape track.
        if client_id and client_secret:
            songs = search_track(args[0])
            self.misc.open_program("start {}".format(songs.get(list(songs.keys())[0])))
            self.misc.focus_window("spotify")
            time.sleep(0.5)
            self.misc.search_screen(image="assets/images/highlighted_song.png", click_center=True)
        else: # Otherwise give the url to create a developer application.
            self.voiceh.speak("No developer application set, please follow the guide on the logged link in terminal")
            self.voiceh.speak("Afterwards set the client id/secret in play song function")
            print("https://developer.spotify.com/documentation/general/guides/app-settings/?fbclid=IwAR1xHP62ZxxsI2GqAibc0tE5EPEUv0_G_uAkPoMQODtJz_il8tEsJbX5P0c#register-your-app")

    """ Miscellaneous """
    def tell_me_a_joke(self):
        print("Telling a joke")
        # Fetch jokes from API
        url = "https://official-joke-api.appspot.com/random_ten"
        url_response = eval(requests.get(url).text)
        random_joke = random.choice(url_response)
        self.voiceh.speak(random_joke["setup"])
        self.voiceh.speak(random_joke["punchline"])

    def movie_suggestion(self, *args, **kwargs):
        def scrape_movie_list(genre):
            # if a genre has been set, scrape list from IMDB
            page = requests.get("https://www.imdb.com/search/title/?genres={genre}".format(genre=genre))
            soupobj = bs4.BeautifulSoup(page.text, features="html.parser")
            raw_movie_list = soupobj.find_all("div", class_="lister-item-content")

            movies = {}
            # Loop through all movies & get title & description from each movie.
            for movie in raw_movie_list:
                subsoup = bs4.BeautifulSoup(str(movie), features="html.parser")
                title = [i for i in subsoup.find_all("a") if "title/tt" in str(i) and not "vote" in str(i)][0]
                title = str(title)[str(title).find('">') + 2:str(title).find('</')]

                for indx, i in enumerate(subsoup.find_all("p", class_="text-muted")):
                    if indx != 1:
                        continue
                    description = str(i)[str(i).find("\n") + 1:str(i).find("</p")].strip()
                    movies[title] = description
            return movies

        def get_genre(search_str=None):
            genre = ["horror", "action", "sci-fi", "thriller", "crime", "mystery"]
            if search_str:
                search = self.misc.stringset_comparer(search_str, genre)
                if search:
                    return search
                else:
                    return
            else:
                return random.choice(genre)

        genre = get_genre(args[0]) if args else get_genre()
        if genre:
            movies = scrape_movie_list(genre)

            # Select a random movie from dictionairy
            random_movie = random.choice(list(movies.keys()))
            self.voiceh.speak(random_movie)
            self.voiceh.speak(movies[random_movie])

            # Print in terminal if something wasnt audible given the option to read it:
            print("Name: %s\nDescription: %s" % (random_movie, movies[random_movie]))
            time.sleep(1) # Add sleep otherwise, command question was to fast / unatural.

    def commands(self):
        self.voiceh.speak("Voice commands are: ")
        for i in [k for k in list(self.__class__.__dict__.keys()) if "__" not in k]:
            i = i if not "_" in i else i.replace("_", " ")
            self.voiceh.speak(i)


if __name__ == "__main__":
    print("CommandHandler isnt an executable class, run program from Main.py")
    exit(0)