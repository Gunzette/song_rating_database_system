from structure_classes import Rating, Song, Album, Album_Container
import search_functions

container = Album_Container()

song1 = search_functions.search_song(container, "Test Song 2")

print(song1.average)