from flask import Flask,render_template,request, redirect, url_for, g, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
#import jwt

import sys
import datetime
#import bcrypt
import traceback

#from tools.eeg import get_head_band_sensor_object


from db_con import get_db_instance, get_db

#from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

#  This code sets up a web application with specific API endpoints for executing functions

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"


#Create our app
app = Flask(__name__)
#add in flask json
FlaskJSON(app)

from tools.logging import logger
from flask_socketio import SocketIO
import video_manager

socketio = SocketIO(app, manage_session=False)

#g is flask for a global var storage 
def init_new_env():
    #To connect to DB
    if 'db' not in g:
        g.db = get_db()

    if 'hb' not in g:
        g.hb = get_head_band_sensor_object()

    #g.secrets = get_secrets()
    #g.sms_client = get_sms_client()

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/') #endpoint
def index():
    return redirect('/static/index.html')


@app.route("/secure_api/<proc_name>",methods=['GET', 'POST'])
#@token_required
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp



@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp


@socketio.on('connect')
def handle_message():
    print('***\nWebsocket connected on servers end \n***')
 #Call This function and pass in the new video path, when it is time to change the clients video.   
def changeVideo(videoPath):
        print(videoPath)
        socketio.emit('change_video',videoPath)

@socketio.on('client-connection-ack')
def handle_message():
    print("***\nserver has been notified that websocket is connected on clients end\n***")

@app.route('/get-videos-list')
def get_list():
    items = video_manager.getVideoNames()
    print(items)
    return jsonify(items)

@app.route('/get-all-video-paths')
def get_both_list():
    items = video_manager.getAllVideoPaths()
    print(items)
    return jsonify(items)
@app.route('/get-fun-videos-list')
def get_fun_list():
    items = video_manager.getFunVideoNames()
    print(items)
    return jsonify(items)

@app.route('/get-educational-videos-list')
def get_edu_list():
    items = video_manager.getEducationalVideoNames()
    print(items)
    return jsonify(items)

@socketio.on('new_video')
def handle_new_video(data):
    print(data)
    video_name = data['name']
    changeVideo(video_name)

@app.route('/images')
def images():
    videoNames = video_manager.getEducationalVideoNames()  # Replace with actual image paths
    thumbnailPaths = []
    for imageName in videoNames:
        imageName += ".png"
        imageName = "thumbnails/" + imageName
        thumbnailPaths.append(imageName)
    for name in thumbnailPaths:
        print(name)
    return jsonify(thumbnailPaths)

@app.before_first_request
def before_first_request():
    print("before first request")
    video_manager.update_thumbnails()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

