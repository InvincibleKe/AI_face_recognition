import sys
import os
import socketio
import base64
import json
import numpy as np
import time
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")

name_space = '/face-recognize'
sio = socketio.Client()
def img_to_base64(img_path):
    with open(img_path, 'rb')as read:
        b64 = base64.b64encode(read.read())
    return b64

@sio.on('connect')
def on_connect():
    """创建连接"""
    print('I am connected!')

@sio.on('single_recognition_response', namespace=name_space)
def on_message(msg):
    print('I received a single message!')
    print(json.loads(msg).get('code'))
    img_b64 = img_to_base64('asserts/3.jpg')
    sio.emit('multi_recognition', json.dumps({'stream': img_b64}, cls=MyEncoder, indent=4), namespace='/multi-face-recognize')

@sio.on('multi_recognition_response', namespace='/multi-face-recognize')
def on_multi(msg):
    print('I received a multi message!')
    print(json.loads(msg).get('code'))
    img_b64 = img_to_base64('asserts/4.jpg')
    sio.emit('single_recognition', json.dumps({'stream': img_b64}, cls=MyEncoder, indent=4), namespace=name_space)

@sio.on('disconnect')
def on_disconnect():
    """关闭连接"""
    print('I m disconnected!')

@sio.on('callback message', namespace=name_space)
def my_event_handler(data):
    # 客户端接收服务端的回调消息
    print("my receive new msg:", data)
    # 接收完消息关闭连接
    sio.disconnect()
    return "ok!"

# 建立连接对象
print('1')
sio.connect('http://dev.1msoft.cn:8888')
print(2)
img_b64 = img_to_base64('asserts/4.jpg')
print(3)
sio.emit('single_recognition', json.dumps({'stream': img_b64},cls=MyEncoder,indent=4), namespace=name_space)
print('4')

print('5')
#sio.sleep(0)
