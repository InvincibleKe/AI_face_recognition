#!/usr/bin/env python
# encoding: utf-8
import cv2
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect
import json
import sys
import os
import base64
import numpy as np
from threading import Lock
import time
from flask import Flask, make_response, jsonify
import eventlet
from face_input import face_input, face_detect
from image_recognition_multi import image_recognition_multi
from image_recognition_single import image_recognition_single
import mysql

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
thread = None
thread_lock = Lock()

eventlet.monkey_patch()
async_mode = None
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins='*', message_queue='redis://127.0.0.1:6379', async_mode='eventlet')

now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

# openCV mat 格式转为 base64 格式
def cv_base64(img_cv):
    image = cv2.imencode('.jpg', img_cv)[1]
    base64_data = str(base64.b64encode(image))[2:-1]
    return base64_data

# base64 格式转为 openCV mat 格式
def base64_cv(img_64):
    imgData = base64.b64decode(img_64)
    nparr = np.fromstring(imgData, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

# 多人人脸识别接口
@socketio.on('multi_recognition', namespace='/multi-face-recognize')
def multi_recognition_socket(msg):
    msg = json.loads(msg)
    img_64 = msg.get('stream')
    img = base64_cv(img_64)
    print('recognition_image_multi before')
    code, uids, img_detect = image_recognition_multi(img)
    img_detect_64 = cv_base64(img_detect)
    if code == 0:
        message = '多人识别成功'
    else:
        message = '无法检测到人脸'

    res = {'code': code, 'message': message, 'data': {'userIds': uids, 'stream': img_detect_64}}
    res = json.dumps(res, cls=MyEncoder, indent=4)
    emit('multi_recognition_response', res, namespace='/multi-face-recognize')
    print('send multi')

# 单人人脸识别接口
@socketio.on('single_recognition', namespace='/face-recognize')
def single_recognition_socket(msg):
    print('single_recognition connected')
    print(type(msg))
    msg = json.loads(msg)
    img_64 = msg.get('stream')
    print(img_64[:100])
    img = base64_cv(img_64)
    uid = image_recognition_single(img)
    # uid='123'
    print(uid)
    if uid == 1:
        message = '无法检测到人脸'
        code = 1
        uid = ''
    elif uid ==2:
        message = '检测到多张人脸'
        code = 2
        uid = ''
    elif uid == 3:
        message = '人脸库无此人'
        code = 3
        uid = ''
    elif uid == 4:
        message = '人脸库为空'
        code = 4
        uid = ''
    else:
        message = '单人识别成功'
        code = 0
    res = {'code': code, 'message': message, 'data': {'userId': uid, 'photo': img_64}}
    res = json.dumps(res, cls=MyEncoder, indent=4)
    emit('single_recognition_response', res, namespace='/face-recognize')
    # emit('single_recognition_response', {'code':0}, namespace='/face-recognize')
    print('single send')

# 人脸录入接口
@socketio.on('face_input', namespace='/face-record')
def input_socket(msg):
    msg = json.loads(msg)
    uid = msg.get('userId')
    memo = msg.get('memo')
    img_64 = msg.get('stream')
    # from base64 to cv mat
    img = base64_cv(img_64)
    ret = face_input(img, uid, memo)
    code = ret
    data = {'userId': uid, 'photo': img_64}
    if code == 0:
        message = '处理成功'
    elif code == 1:
        message = '无法检测到人脸'
    else:
        message = '检测到多个人脸'
    res = {'code': code, 'message': message, 'data': data}
    res = json.dumps(res, cls=MyEncoder, indent=4)
    emit('face_input_response', res, namespace='/face-record')
# 单人人脸检测接口
@socketio.on('face_detect', namespace='/face-detect')
def detect_socket(msg):
    msg = json.loads(msg)
    img_64 = msg.get('stream')
    # from base64 to cv mat
    img = base64_cv(img_64)
    code = face_detect(img)
    if code == 1:
        message = '无法检测到人脸'
    elif code == 2:
        message = '检测到多个人脸'
    elif code == 0:
        message = '检测到1个人脸'
    res = {'code': code, 'message': message, 'stream': img_64}
    res = json.dumps(res, cls=MyEncoder, indent=4)
    emit('face_detect_response', res, namespace='/face-detect')
# 数据初始化（清理）
@app.route('/init-data')
def clean():
    code = mysql.data_clean()
    if code == 0:
        message = "数据清理成功"
    elif code == 1:
        message = "删除特征表失败"
    elif code == 2:
        message = '删除人脸表失败'
    else:
        message = '删除用户表失败'
    res = {'code': code, 'message': message}
    res = make_response(jsonify(res))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    return res

@app.route('/')
def hello():
    return 'Hello World! server start！'

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)

    '''
    init()
    image = cv2.imread('images/4-2.jpeg')
    uid = recognition_image_single(image)
    print(uid)
    while(True):
        uid = recognition_image_single(image)
        print(uid)
        uids = recognition_image_multi(image)[1]
        print(uids)'''
