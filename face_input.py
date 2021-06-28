import face_recognition
import uuid
import mysql
import cv2
def face_detect(image):
    face_marks = face_recognition.face_landmarks(image)
    num = len(face_marks)
    if num == 1:
        return 0
    elif num == 0:
        return 1
    else:
        return 2
def face_input(image, uid, memo):
    face_marks = face_recognition.face_landmarks(image)
    num = len(face_marks)
    if num == 1:
        fid = uuid.uuid1()
        feature = face_recognition.face_encodings(image)[0]
        mysql.insert_user_info(uid, memo)
        mysql.insert_face_feature(fid, feature.tobytes())
        mysql.insert_uid_fid(uid, fid)
        return 0
    elif num == 0:
        return 1
    else:
        return 2

if __name__ == '__main__':
    img = cv2.imread('asserts/test11.jpg')
    uid = uuid.uuid1()
    ret = face_input(img, uid, '池爱晶')
    print(ret)