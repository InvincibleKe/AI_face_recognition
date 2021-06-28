# coding=UTF-8

import requests
#r = requests.get("http://0.0.0.0:5000/init-data")
r = requests.get("http://dev.1msoft.cn:8888/init-data")
print(r.json())