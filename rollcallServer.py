from flask import Flask,request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from rollcallSocket import zuvio
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app, cors_allowed_origins="*")
app.host = 'localhost'

# @app.route("/")
# def hello():
#     return ({"msg":"Hello world"})

@socketio.on('connect')
def connect_msg():
    print("connect")
    emit('getMessage',{'data':'data'})

@socketio.on('disconnect')
def disconnect(msg):
    print("disconnect")
    emit({})
@socketio.on('getMessage')
def getMessage(msg):
    print(msg)
# @app.route("/",methods = ['POST'])
# def getInfo():
#     if request.method == 'POST':
#         userInfo = request.values['userInfo']
#         print(userInfo)
if __name__ == "__main__":
    socketio.run(app)