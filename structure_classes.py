from statistics import mean
from json import load, dump

# Functions needed for the sort_abums_...() methods of Album_Container
def get_release_year(album):
    return album.release_year
def get_artist(album):
    return album.artist
def get_average(album):
    return album.calc_average()


class Rating:
    def __init__(self, musical: int, creative: int, catchy: int):
        # Defines the rating attributes
        self.musical = musical
        self.creative = creative
        self.catchy = catchy

        # Calculates the average of the three ratings (with musical having double the weight)
        self.avg = round(mean([musical, musical, creative, catchy]), 2)

    def modify_rating(self, new_musical, new_creative, new_catchy):
        # Changes the rating attributes to their new values
        self.musical = new_musical
        self.creative = new_creative
        self.catchy = new_catchy

        # Recalculates the average
        self.avg = round(mean([new_musical, new_musical, new_creative, new_catchy]), 1)

class Song:
    def __init__(self, name: str, rating: Rating):
        # Initializes name and rating
        self.name = name
        self.rating = rating

    def to_dict(self):
        # Transforms the Song object into a dictionary and returns it
        ret_dict = {
            "name": self.name,
            "rating": {
                "average": self.rating.avg,
                "musical": self.rating.musical,
                "creative": self.rating.creative,
                "catchy": self.rating.catchy
            }
        }
        return ret_dict

    def modify_name(self, new_name):
        self.name = new_name

class Album:
    def __init__(self, name: str, artist: str, release_year: int, song_list: list[Song] = []):
        # Initializes the basic attributes
        self.name: str = name
        self.artist: str = artist
        self.release_year: int = release_year

        # Creates an Empty list if initialized without songs/adds all songs it is initialized with.
        self.song_list: list[Song] = song_list

    def add_song(self, song: Song, placement: int=-1):
        # Adds a song. If no placement in the List is specified, it will be added at the end of the list.
        if placement == -1:
            self.song_list.append(song)
        elif placement > -1:
            self.song_list.insert(placement, song)

    def remove_song(self, song_name):
        for song_index in range(len(self.song_list)):
            if self.song_list[song_index].name == song_name:
                self.song_list.pop(song_index)
                break
        else:
            print("The song name you entered was not in this album")

    def calc_average(self):
        # Gets a list of all song average scores
        song_averages = []
        for song in self.song_list:
            song_averages.append(song.rating.avg)

        # Calculates the average of the averages and returns it.
        average = round(mean(song_averages), 2)
        return average
    
    def to_dict(self):
        # Transforms the Album object into a dictionary and returns it
        ret_dict = {
            "name": self.name,
            "artist": self.artist,
            "release_year": self.release_year,
            "album_average": self.calc_average(),
            "songs": [song.to_dict() for song in self.song_list]
        }
        return ret_dict

class Album_Container:
    def __init__(self):
        # Fetches the Album list by calling the read_database() function
        self.album_list = self.read_database()

    def read_database(self) -> list[Album]:
        # Reads the json database and converts it into a list of Album objects
        with open("database.json", "r") as f:
            json_albums = load(f)["albums"]

        ret_list = []

        for album in json_albums:
            ret_list.append(Album(album["name"], album["artist"], album["release_year"], self.rebuild_songs(album["songs"])))

        return ret_list
    
    def rebuild_songs(self, songlist: list[dict]):
        # Rebuilds the Json song list into song objects
        ret_list = []
        for song in songlist:
            ret_list.append(Song(song["name"], Rating(song["rating"]["musical"], song["rating"]["creative"], song["rating"]["catchy"])))
        return ret_list


    #Functions that sort the album list based on release year, artist or average
    def sort_albums_by_release_year(self):
        self.album_list.sort(key=get_release_year)
    def sort_albums_by_artist(self):
        self.album_list.sort(key=get_artist)
    def sort_albums_by_average(self):
        self.album_list.sort(key=get_average, reverse=True)


    def write_database(self) -> None:
        # Puts the current state in a dictionary and writes it into the json database
        dump_dict = {"albums": [album.to_dict() for album in self.album_list]}
        with open("database.json", "w") as f:
            dump(dump_dict, f, indent=4, ensure_ascii=False)

    def add_album(self, album: Album) -> None:
        self.album_list.append(album)