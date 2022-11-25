import cv2
import os
import moviepy.editor as mpe


def add_music(videoName, audioPath):
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

images = [img for img in os.listdir(imageFolder) if img.endswith(".png") or img.endswith(".jpeg") or img.endswith(".jpg")]
frameTime = [5] * len(images)
fps = 1
frameSize = (1920, 1200)

video = cv2.VideoWriter(videoName, MP4CODEC, fps, frameSize)

for image, i in zip(images, frameTime):
    sec = i * fps
    while(sec != 0):
        sec -= 1
        video.write(cv2.imread(os.path.join(imageFolder, image)))

cv2.destroyAllWindows()
video.release()

add_music(videoName, os.path.join(audioFolder, audioName))
