import os
import hashlib


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
    
    

if __name__ == '__main__':
    video_names = getVideoNames()
    for key in video_names:
        print(video_names[key])


#video Manager
# get video names
# update list