from structure_classes import Song, Album, Album_Container

def search_song(container: Album_Container, name: str) -> Song:
    for album in container.album_list:
        for song in album.song_list:
            if song.name == name:
                return song
    else:
        print("Song was not found")
        return None
    

def search_album(container: Album_Container, name: str) -> Album:
    for album in container.album_list:
        if album.name == name:
            return album
    else:
        print("Album was not found")
        return None