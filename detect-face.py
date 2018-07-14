#!/usr/bin/env python
import numpy as np
import cv2 as cv
import glob
import re

face_cascade = cv.CascadeClassifier(cv.haarcascades + 'haarcascade_frontalface_default.xml')

def load_image(filename):
    return cv.imread(filename)

def detect_face(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    h, w = img.shape[:2]
    size = (w, h)
    center = (w / 2, h / 2)

    imgs = []
    for angle in range(0, 180):
        for angle in [angle, -angle]:
            rotation_matrix = cv.getRotationMatrix2D(center, angle, 1.0)
            img_rot = cv.warpAffine(img, rotation_matrix, size, flags = cv.INTER_CUBIC)
            faces = face_cascade.detectMultiScale(img_rot, 1.3, 5)
            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    imgs.append(img[y : y + h, x : x + w])
                return imgs
    return imgs

def show(img, faces):
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w), (y + h), (255, 0, 0), 2)
    cv.imshow('img',img)
    cv.waitKey(300)

def save(img, filename):
    cv.imwrite(filename, img)

def detect_face_in_directory(directory):
    files = glob.glob(directory + '/**/*.jpg')
    print("files in", directory, len(files))

    img = load_image('train/japan/6525274.jpg')
    faces = detect_face(img)
    for filename in files:
        img = load_image(filename)
        faces = detect_face(img)

        for idx, face in enumerate(faces):
            save_filename = re.sub(r'\.jpg', '-%d.jpg' % idx, filename.replace(directory, 'face_' + directory))
            cv.imwrite(save_filename, face)

for directory in ['train', 'test']:
    detect_face_in_directory(directory)
