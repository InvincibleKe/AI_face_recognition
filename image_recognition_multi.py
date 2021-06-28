import face_recognition
import cv2
import mysql
import image_merge
import cv_ChineseText
import numpy as np

icon_tick = cv2.imread('icons/icon_tick.png', cv2.IMREAD_UNCHANGED)
text_background = cv2.imread('icons/text_background.png', cv2.IMREAD_UNCHANGED)
font_face = cv2.FONT_HERSHEY_COMPLEX
font_scale = 2
thickness = 2

# 画脸框
def draw_faceBorder(img, pt1, pt2, color = (255,161,14), thickness = thickness):
    x1, y1 = pt1
    x2, y2 = pt2
    d = round((x2-x1)/8)
    r = round(d/4)
    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
    return img

# 画出人脸上面的标签
def draw_label(img, text, faceFrame_pt1, faceFrame_pt2):
    text = text + '(已签到)'
    x1, y1 = faceFrame_pt1
    x2, y2 = faceFrame_pt2
    faceFrame_width = x2 - x1
    faceFrame_height = y2 - y1
    text_width, text_height = cv2.getTextSize(text, font_face,font_scale, thickness)[0]
    #print(cv2.getTextSize(text, font_face,font_scale, thickness))
    text_y = y1 - 112
    text_x = x1 + round((faceFrame_width - text_width)/2) + 32
    tick_y = text_y - 2
    tick_x = text_x - 82
    background_y = tick_y - 14
    background_x = tick_x - 24
    text_background0 = cv2.resize(text_background, (text_width + 150, 94))
    #text_background0 = text_background
    background_height = text_background0.shape[0]
    background_width = text_background0.shape[1]
    #icon_tick0 = cv2.resize(icon_tick, (29,29))
    img = image_merge.merge_img(img, text_background0, background_y, background_y+background_height, background_x, background_x+background_width)
    img = image_merge.merge_img(img, icon_tick, tick_y, tick_y+60, tick_x, tick_x+60)
    img = cv_ChineseText.cv2ImgAddText(img, text, text_x, text_y)
    return img

# 返回带脸框的图片
def draw_faceFrame(imageData, faces):
    for i in range(0, faces.faceNum):
        # 画出人脸框
        ra = faces.faceRect[i]
        imageData.image = draw_faceBorder(imageData.image, (ra.left, ra.top),
                      (ra.right, ra.bottom))
    return imageData.image

# 返回用户的memo
def get_memo(users, uid):
    if len(users)>0:
        for item in users:
            if item[0] == uid:
                return item[1]
        return 1
    else: return 1

def image_recognition_single(feature, features):
    print(len(features))
    if len(features) != 0:
        distance_min = 100000
        fid_min = 0
        for item in features:
            fid = item[0]
            feature_db = np.frombuffer(item[1])
            result = face_recognition.compare_faces([feature_db], feature, 0.4)
            if result[0] == True:
                distance = face_recognition.face_distance([feature_db], feature)
                if distance < distance_min:
                    distance_min = distance
                    fid_min = fid
        if fid_min != 0:
            uid = mysql.getUid(fid_min)
            return uid
        else: return 1
    else: return 1

def image_recognition_multi(img):
    uids = []
    face_locations = face_recognition.face_locations(img)
    face_num = len(face_locations)
    if face_num == 0:
        code = 1
        return code, uids, img
    else:
        code = 0
        features = mysql.get_faceFeatures()
        face_encodings = face_recognition.face_encodings(img, face_locations)
        for i in range(0, face_num):
            uid = image_recognition_single(face_encodings[i], features)
            # 画出人脸框img
            top, right, bottom, left=face_locations[i]
            img = draw_faceBorder(img, (left, top),
                                              (right, bottom))
            if uid != 1:
                uids.append(uid)
                text = mysql.get_faceInfo(uid)
                # text = get_memo(users, uid)
                print(text)
                if text != 1:
                    img = draw_label(img, text, (left, top),
                                                 (right, bottom))
        return code, uids, img

if __name__ == '__main__':
    img = cv2.imread('asserts/4.jpg')
    uids, image = image_recognition_multi(img)
    print(uids)
    cv2.namedWindow('hhh', 0)
    cv2.imshow('hhh', image)
    cv2.waitKey(0)