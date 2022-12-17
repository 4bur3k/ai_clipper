import lyricsgenius as genius

clientAccessToken = 'CXXnPdAycfaibUkry8LWSDmB5ojnrXUVUXxL7HFvaX9kQQsJZjm3hOPTgayuA8iG'
api = genius.Genius(clientAccessToken)

song = None
while song is None:
    songName = input()
    song = api.search_song(songName) # get song using song name from site
    if song is None:
        print("Такой песни не найдено, попробуйте снова")
lyrics = [row for row in song.lyrics.split('\n')[1:] if len(row) > 0 and row[0] != "["] # delete title and technic information, like [verse], [chorus] etc.

embedEdge = -1
for i in range(len(lyrics[-1]) - 1,-1,-1): # delete the end of last line. It looks like 'row + 382embed', so, we need to delete '382embed'
    if lyrics[-1][i].isdigit():
        embedEdge = i

lyrics[-1] = lyrics[-1][:embedEdge]
print(lyrics) # we got the list of song's lines
