import cv2
import numpy as np
import face_recognition as fr
import dlib
import time
import os

path = 'Image DataSet'
images = []    # creating a list to store multiple images
ClassNames = []     # this would store the name of all the images
imgList = os.listdir(path)      # extracting the list of images from the folder
print('Extracting the Images from the Data Set folder! ',imgList)      # checking if we have extracted them correctly

for cl in imgList:      # now storing the multiple images into the image list created above
    CurrentImage = cv2.imread(f'{path}/{cl}')      # reading the current image through open cv image read function
    images.append(CurrentImage)     # appending the images into the image list
    ClassNames.append(os.path.splitext(cl)[0])      # extracting only the image name and not the extension
print('The Names of the Images in the Data Set Folder are: ',ClassNames)       # displays the names of the images along with their extensions


def GenerateEncodings(images):
    Encodelist = []  #creating an empty list to store the image encodings data in it
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  # converting bgr to rgb
        encode = fr.face_encodings(img)[0]  #
        Encodelist.append(encode)
    return Encodelist

KnownEncodeList=GenerateEncodings(images)
print('Encodings of the Images have been completed!')



# initiating the webcam

cam = cv2.VideoCapture(0)


while True:
    Success, img = cam.read()
    ImageScale = cv2.resize(img,(0,0),None,0.25,0.25)
    ImageScale = cv2.cvtColor(ImageScale,cv2.COLOR_BGR2RGB)

    CurrentFrame = fr.face_locations(ImageScale)
    EncodeCurrentFrame = fr.face_encodings(ImageScale,CurrentFrame)


    for EncodeFace, FaceLoc in zip(EncodeCurrentFrame,CurrentFrame):
        matches = fr.compare_faces(KnownEncodeList,EncodeFace)
        Facedis = fr.face_distance(KnownEncodeList,EncodeFace)
        print('Minimal Face Distances: ', Facedis)
        matchIndex = np.argmin(Facedis)

        if matches[matchIndex]:
            Name = ClassNames[matchIndex].upper()
            print('Name: ',Name)
            y1,x2,y2,x1 = FaceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,Name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    cv2.imshow('WebCam',img)
    cv2.waitKey(1)

































