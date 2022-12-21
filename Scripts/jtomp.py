import cv2
import os
import moviepy.editor as mpe
from mutagen.mp3 import MP3


def add_music(videoName, audioPath): # add music to video which was already generated
    video_clip = mpe.VideoFileClip(videoName)
    audio_clip = mpe.AudioFileClip(audioPath)
    audio_clip = audio_clip.subclip(0, video_clip.end)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile('result.mp4')


MP4CODEC = 0x7634706d

imageFolder = 'images'
audioFolder = 'audio'
videoName = 'result__without_music.mp4'
audioName = [msc for msc in os.listdir(audioFolder) if msc.endswith(".mp3")][0]

audioInfo = MP3(os.path.join(audioFolder, audioName))
clipLengthSecs = int(audioInfo.info.length) # get audio length in seconds
images = [img for img in os.listdir(imageFolder) if img.endswith(".png") or img.endswith(".jpeg") or img.endswith(".jpg")]
frameTime = [int(clipLengthSecs / len(images))] * len(images)  # create list of time for every frame in video
print(frameTime)
fps = 1
imgShape = cv2.imread(os.path.join(imageFolder, images[0])).shape
frameSize = (imgShape[1], imgShape[0])  # define video size

images = ['img' + str(i) + '.jpg' for i in range(len(images))]  # generate list of all file names in right order

video = cv2.VideoWriter(videoName, MP4CODEC, fps, frameSize)  # create empty video

for image, i in zip(images, frameTime):
    sec = i * fps
    while(sec != 0):
        sec -= 1
        video.write(cv2.imread(os.path.join(imageFolder, image)))

cv2.destroyAllWindows()
video.release()

add_music(videoName, os.path.join(audioFolder, audioName))
