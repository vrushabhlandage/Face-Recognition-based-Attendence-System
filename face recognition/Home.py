import cv2
import numpy as np
import face_recognition
import os
import streamlit as st
from datetime import datetime
import sqlite3
import pandas as pd

now = datetime.now()

nowtime = now.strftime("%H:%M")

nowdate = now.date()

conn = sqlite3.connect('database.db', check_same_thread=False)

c = conn.cursor()
#
# # cnx = sqlite3.connect('database.db')
# df = pd.read_sql_query('SELECT * FROM attendance WHERE dt = ?', nowdate)
#
# id_list = list(df['id'])
#
# print(id_list)

#
# c.execute('SELECT id FROM attendance WHERE dt = ?', (nowdate,))
#
# id_list = (c.fetchall())
#

# print(id_list)
# print(type(id_list))
#
# outputlist = [item for t in id_list for item in t]
#
#
# print(outputlist)
# print(type(outputlist))
#

def function_attendance(i, x, y, z):
    c.execute('CREATE TABLE IF NOT EXISTS attendance(id INTEGER,name TEXT,dt DATE,tm TIME);')
    c.execute('INSERT INTO attendance VALUES(?,?,?,?)', (i, x, y, z))
    conn.commit()
    st.success(separated_name + " attendance marked successfully ")



st.title("Face Recognition System")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
path = 'images'
images = []
personName = []
myList = os.listdir(path)
# print(myList)

for cu_img in myList:
    current_img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_img)
    personName.append(os.path.splitext(cu_img)[0])
# print(personName)


def faceEncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist


encodeListKnown = faceEncodings(images)
print("All Encodings Completed!!!")

camera = cv2.VideoCapture(0)

while run:
    ret, frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodeCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personName[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)

            # separate name and id

            s_id = name[0:4]

            separated_id = int(s_id)

            separated_name = name[4:]

            cv2.putText(frame, separated_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            c.execute('SELECT id FROM attendance WHERE dt = ?', (nowdate,))

            id_list = (c.fetchall())

            # print(id_list)
            # print(type(id_list))

            outputlist = [item for t in id_list for item in t]

            # print(outputlist)
            # print(type(outputlist))

            if separated_id not in outputlist:
                function_attendance(separated_id, separated_name, nowdate, nowtime)

    FRAME_WINDOW.image(frame)

else:
    st.write('Stopped')
