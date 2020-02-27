#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  25 14:11:40 2020
@author: dev
"""
#%%
import mysql.connector as sql
import face_recognition
import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime

mydb=sql.connect(host='localhost',user='root',password='password')
mycursor = mydb.cursor()
mycursor.execute("use employee")

x = datetime.datetime.now()
currdate=x.date()
currdate=str(currdate)

mycursor.execute("select * from employee.employee")
count=mycursor.fetchall()
print('count=',count.__len__())
def todayAttendance():
    sql1="SELECT name FROM employee.employee where date = %s" 
    val=(currdate,)
    mycursor.execute(sql1,val)
    myresult=mycursor.fetchall()
    # print("sucessfully fetched")
    # =============================================================================
    print(myresult)
    presentList=[]
    for name in myresult:
        presentList.append(name[0])
        
    return presentList    

#%%
video_capture = cv2.VideoCapture(0)
Ajit = face_recognition.load_image_file("/home/dev/Pictures/employeesPics/ID.png")
ajit_encoding = face_recognition.face_encodings(Ajit)[0]

tom_image = face_recognition.load_image_file("/home/dev/Pictures/index.jpeg")
tom_face_encoding = face_recognition.face_encodings(tom_image)[0]

Ak = face_recognition.load_image_file("/home/dev/Pictures/employeesPics/akID.png")
ak_encoding = face_recognition.face_encodings(Ak)[0]

Akshay = face_recognition.load_image_file("/home/dev/Pictures/employeesPics/Akshay.png")
akshay_encoding = face_recognition.face_encodings(Akshay)[0]

Snehal = face_recognition.load_image_file("/home/dev/Pictures/employeesPics/Snehal.png")
snehal_encoding = face_recognition.face_encodings(Snehal)[0]

Bhagyashri = face_recognition.load_image_file("/home/dev/Pictures/employeesPics/Bhagyashri.png")
bhagyashri_encoding = face_recognition.face_encodings(Bhagyashri)[0]

known_face_encodings = [
    ajit_encoding,
    tom_face_encoding,
    ak_encoding,
    akshay_encoding,
    snehal_encoding,
    bhagyashri_encoding
]
known_face_names = [
    "AJIT JADHAV",
    "TOM HARDY",
    "ATUL SIR",
    "AKSHAY KEDAR",
    "SNEHAL SHETE",
    "BHAGYASHRI NIKAM"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
presentList=todayAttendance()
while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]
    
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                IsInList=presentList.count(name)
                if IsInList==0:
                    x = datetime.datetime.now()
                    empid=count.__len__()+1
                    sql = "INSERT INTO employee.employee (idemployee, name, timeIN, date) VALUES (%s,%s, %s,%s)"
                    val = (empid,name,x.time(),x.date() )
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print('\n\n\n\n PRESENTI LAGLI EEEVVVVVVVVVVVVVVVVV \n\n\n\n')
                    presentList=todayAttendance()
                    
                else:
                    print(name+' TU AGODRCH PRESENTI LAVLIY LKAA \n')
            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video_capture.release()
cv2.destroyAllWindows()
