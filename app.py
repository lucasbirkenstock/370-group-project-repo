from flask import Flask, render_template, request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import sys
import datetime
import traceback
import socket

from tools.eeg import get_head_band_sensor_object
from db_con import get_db_instance, get_db

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"

app = Flask(__name__)
FlaskJSON(app)

def init_new_env():
    if 'db' not in g:
        g.db = get_db()

    if 'hb' not in g:
        g.hb = get_head_band_sensor_object()

@app.route('/')
def index():
    return redirect('/static/index.html')

@app.route("/secure_api/<proc_name>", methods=['GET', 'POST'])
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")
    init_new_env()
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.' + proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500, data=ERROR_MSG)
    return resp

@app.route("/open_api/<proc_name>", methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")
    init_new_env()
    resp = ""
    try:
        fn = getattr(__import__('open_calls.' + proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500, data=ERROR_MSG)
    return resp

# Add this block at the end of app.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 80))

@app.route('/login', methods=['POST'])
def login():
    try:
        client.send(request.form['username'].encode())
        client.recv(1024)  
        client.send(request.form['password'].encode())
        result = client.recv(1024).decode()
        return result
    except Exception as e:
        return f"Error: {e}"
