import os
import hashlib

import cv2
import os
from PIL import Image

directory = 'static/videos/'

def setDirectory(new_directory):
    directory = new_directory
def videoPath(videoname):
    mp4_name = directory + videoname + ".mp4"
    return mp4_name
def getVideoNames():
    names = {}
    namesList = []
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            name, extension = os.path.splitext(filename)
            namesList.append(name)
            names [hashlib.sha256(name.encode()).hexdigest()] = name
    return namesList
    


video_folder = 'static/videos'
thumbnail_folder = 'static/thumbnails'

def update_thumbnails():
    if not os.path.exists(thumbnail_folder):
        os.makedirs(thumbnail_folder)

    for filename in os.listdir(video_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(video_folder, filename)
            thumbnail_name = filename.replace('.mp4', '.png')
            thumbnail_path = os.path.join(thumbnail_folder, thumbnail_name)

            cap = cv2.VideoCapture(video_path)
            success, frame = cap.read()

            if success:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                img = Image.fromarray(rgb_frame)
                img.save(thumbnail_path)

                print(f"{filename} thumbnail created")
            else:
                print(f"{filename} thumbnail failed")
            cap.release()
   

if __name__ == '__main__':
    video_names = getVideoNames()
    for key in video_names:
        print(video_names[key])


#video Manager
# get video names
# update list