import os
import requests

from flask import Flask, session, request, redirect, flash, jsonify
from flask_socketio import SocketIO, emit
from flask import render_template
from dotenv import load_dotenv
from flask_session import Session

app = Flask(__name__)
socketio = SocketIO(app)
SESSION_TYPE = 'redis'
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'


Session(app)

# Dictionary holding all chatroom chatlogs
chatLogMaster = {'liveRoom':[], 'joinInfo':[]}

@app.route('/')
def index():
    if 'key' in session:
        username = session['key']
        return(render_template('chatrooms.html', username= username))
    else:
        return(render_template('displayname.html'))


@app.route('/registername', methods=['POST','GET'])
def registername():
    # create session for user with their username
    username = request.form.get('username')
    session['key'] = username
    if request.method == 'POST' or request.method == 'GET' and username in session:
        return(render_template('chatrooms.html', username= username))
    else:
        return(render_template('displayname.html'))


# submit chat should update a dictionary of chats
# will send chatroom name and the chat
@socketio.on('submit_chat')
def chat(data, globalRoom, joinInfo):
    # if not chatroomchatlog in chatLogMaster make it and append chat
    #print(f'globalRoom in python evaluates to {globalRoom}')
    #print(joinInfo)
    chatLogMaster['liveRoom'] = globalRoom
    chatLogMaster['joinInfo'] = joinInfo
    chatText = list(data.values())
    chatData = chatText[0]
    for key, value in chatData.items():
        #lif too many messages, delete back 50
        if key not in chatLogMaster:
            chatLogMaster[key] = [value]
        if len(chatLogMaster[key]) > 99:
                chatLogMaster[key] = ['maximum chats detected... wiping all chats!']
        else:
            # if chatroomlog exists in chatLogMaster, append chat onto end. 
            chatLogMaster[key].append(value)
    print(f'chatlogmaster is {chatLogMaster}')
    emit('chat_entered', chatLogMaster, broadcast=True)



    



