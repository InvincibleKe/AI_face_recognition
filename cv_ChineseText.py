#coding=utf-8
#中文乱码处理
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont

def cv2ImgAddText(img, text, left, top, textColor=(255, 255, 255), textSize=44):
    if (isinstance(img, numpy.ndarray)):  #判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype("font/PingFang_Medium.ttf", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)

    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)