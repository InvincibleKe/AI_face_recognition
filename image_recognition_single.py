import face_recognition
import mysql
import numpy as np
import cv2

def image_recognition_single(img, feature=None, i=0):
    face_marks = face_recognition.face_locations(img)
    num = len(face_marks)
    if num == 1:
        if feature is None:
            feature = face_recognition.face_encodings(img)[i]
        features = mysql.get_faceFeatures()
        print(len(features))
        if len(features) != 0:
            distance_min = 100000
            fid_min = 0
            for item in features:
                fid = item[0]
                feature_db = np.frombuffer(item[1])
                result = face_recognition.compare_faces([feature_db], feature, 0.4)
                print(result)
                if result[0] == True:
                    distance = face_recognition.face_distance([feature_db], feature)
                    if distance < distance_min:
                        distance_min = distance
                        fid_min = fid
            if fid_min != 0:
                uid = mysql.getUid(fid_min)
                return uid
            else: return 3
        else: return 4
    elif num == 0:
        return 1
    else:
        return 2
if __name__ == "__main__":
    img = cv2.imread('asserts/test13.jpg')
    uid = image_recognition_single(img)
    print(uid)