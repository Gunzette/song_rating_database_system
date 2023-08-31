from structure_classes import Rating, Song, Album, Album_Container

container = Album_Container()

container.sort_albums_by_average()

container.write_database()