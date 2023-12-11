import os
import hashlib

import cv2
import os
from PIL import Image

directory = 'static/videos/'
fun_directory = 'static/videos/fun/'

educational_directory = 'static/videos/edu/'


def getAllVideoPaths():
    funlist = getFunVideoPaths()
    edulist = getEducationalVideoPaths()
    lists = [edulist, funlist]
    return lists
def getEducationalVideoNames():
    namesList = []
    for filename in os.listdir(educational_directory):
        if filename.endswith(".mp4"):
            name, extension = os.path.splitext(filename)
            namesList.append(name)
    return namesList

def getFunVideoNames():
    namesList = []
    for filename in os.listdir(fun_directory):
        if filename.endswith(".mp4"):
            name, extension = os.path.splitext(filename)
            namesList.append(name)
    return namesList

def getEducationalVideoPaths():
    namesList = []
    for filename in os.listdir(educational_directory):
        if filename.endswith(".mp4"):
            path = educational_directory + filename
            tokens = path.split('/')
            html_relative_path = '/'.join(tokens[1:])
            namesList.append(html_relative_path)
    return namesList

def getFunVideoPaths():
    namesList = []
    for filename in os.listdir(fun_directory):
        if filename.endswith(".mp4"):
            path = fun_directory + filename
            tokens = path.split('/')
            html_relative_path = '/'.join(tokens[1:])
            namesList.append(html_relative_path)
    return namesList


video_folder = 'static/videos/edu'
thumbnail_folder = 'static/thumbnails'

def update_thumbnails():
    print("Updating thumbnails")
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
    video_names = getEducationalVideoNames()
    for key in video_names:
        print(video_names[key])
    video_names = getFunVideoNames()
    for key in video_names:
        print(video_names[key])


#video Manager
# get video names
# update list