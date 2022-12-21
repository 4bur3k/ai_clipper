import cv2
import os
import moviepy.editor as mpe
from mutagen.mp3 import MP3
import lyricsgenius as genius
import requests
import urllib.request
import re
from bs4 import BeautifulSoup


class ClipMaker:
    songName = ""
    artistName = ""

    def __init__(self, artist, song):
        self.artistName = artist
        self.songName = song

    def jpeg2mp3(self, dirIn, audioPath, dirOut):
        MP4CODEC = 0x7634706d

        imageFolder = dirIn
        audioFolder = audioPath
        videoName = 'result__without_music.mp4'
        audioName = [msc for msc in os.listdir(audioFolder) if msc.endswith(".mp3")][0]

        audioInfo = MP3(os.path.join(audioFolder,audioName))
        clipLengthSecs = int(audioInfo.info.length)  # get audio length in seconds
        images = [img for img in os.listdir(imageFolder) if
                  img.endswith(".png") or img.endswith(".jpeg") or img.endswith(".jpg")]
        frameTime = [int(clipLengthSecs / len(images))] * len(images)  # create list of time for every frame in video
        print(frameTime)
        fps = 1
        imgShape = cv2.imread(os.path.join(imageFolder,images[0])).shape
        frameSize = (imgShape[1],imgShape[0])  # define video size

        images = ['img' + str(i) + '.jpg' for i in range(len(images))]  # generate list of all file names in right order

        video = cv2.VideoWriter(videoName,MP4CODEC,fps,frameSize)  # create empty video

        for image,i in zip(images,frameTime):
            sec = i * fps
            while (sec != 0):
                sec -= 1
                video.write(cv2.imread(os.path.join(imageFolder, image)))

        cv2.destroyAllWindows()
        video.release()

        self.add_music(videoName, os.path.join(audioFolder, audioName))

    def get_song_text(self):
        clientAccessToken = 'CXXnPdAycfaibUkry8LWSDmB5ojnrXUVUXxL7HFvaX9kQQsJZjm3hOPTgayuA8iG'
        api = genius.Genius(clientAccessToken)

        song = None
        song = api.search_song(self.songName)  # get song using song name from site
        if song is None:
            print("Такой песни не найдено, попробуйте снова")
            return None
        lyrics = [row for row in song.lyrics.split('\n')[1:] if
                  len(row) > 0 and row[0] != "["]  # delete title and technic information, like [verse], [chorus] etc.

        embedEdge = -1
        for i in range(len(lyrics[-1]) - 1,-1,
                       -1):  # delete the end of last line. It looks like 'row + 382embed', so, we need to delete '382embed'
            if lyrics[-1][i].isdigit():
                embedEdge = i

        lyrics[-1] = lyrics[-1][:embedEdge]
        print('Песня найдена')
        return lyrics  # we got the list of song's lines

    def download_music(self, audioFold):
        fileFormat = '.mp3'
        songname = self.songName  # Print song name (sometimes it is better to add group name either like "Du hast Rammstein")
        sitename = 'https://ru.hitmotop.com/search?q='
        request = requests.get(sitename + songname.replace(' ','+'))
        soup = BeautifulSoup(request.content,'html.parser')  # got sitepage as special object

        try:
            a = soup.find_all('a',href=re.compile(r'http.*\.mp3'))[0]  # find all music links, but we'll get only first res
        except IndexError:
            return "ERROR: There is no music with such name. Try again, please." # user must print song name again if he has an error
        filename = songname.title().replace(' ','_') + fileFormat
        doc = requests.get(a['href'])
        with open(audioFold + filename,'wb') as f:
            f.write(doc.content)
        return "All right!"

    @staticmethod
    def add_music(videoName,audioPath):  # add music to video which was already generated
        videoClip = mpe.VideoFileClip(videoName)
        audioClip = mpe.AudioFileClip(audioPath)
        audioClip = audioClip.subclip(0,videoClip.end)
        finalClip = videoClip.set_audio(audioClip)
        finalClip.write_videofile('result.mp4')

