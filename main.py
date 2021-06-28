import face_recognition
import numpy as np

known_image = face_recognition.load_image_file("asserts/1.jpg")
unknown_image = face_recognition.load_image_file("asserts/3.jpg")
image2 = face_recognition.load_image_file('asserts/2.jpg')

lyf_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
image2_encoding = face_recognition.face_encodings(image2)[0]

face_encodings = []
face_encodings.append(lyf_encoding)
res = face_recognition.face_distance(face_encodings, unknown_encoding)
face_encodings.append(unknown_encoding)
res2 = face_recognition.face_distance(face_encodings,image2_encoding)
# results = face_recognition.compare_faces([lyf_encoding], unknown_encoding)
# A list of True/False values indicating which known_face_encodings match the face encoding to check

print(type(lyf_encoding))
print(res)
print(res2)