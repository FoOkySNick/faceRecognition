# Training Multiple Faces stored on a DataBase:
# ==> Each face should have a unique numeric integer ID as 1, 2, 3, etc
# ==> LBPH computed model will be saved on trainer/ directory. (if it does not exist, pls create one)
# ==> for using PIL, install pillow library with "pip install pillow"


import cv2
import numpy as np
from PIL import Image
import os
import shutil


class Trainer:
    def __init__(self):
        # Path for face image database
        self.path = 'dataset'

        self.detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def train(self):
        try:
            self.recognizer.read('trainer/trainer.yml')
        except Exception as e:
            pass

        faces, ids = self.get_images_and_labels(self.path)

        print("[INFO] Training faces. It will take a few seconds. Wait ...")
        self.recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        self.recognizer.write('trainer/trainer.yml')  # recognizer.save() worked on Mac, but not on Pi

        # Print the number of faces trained and end program
        face_number = len(np.unique(ids))
        print("[INFO] {0} faces trained. Exiting Program".format(face_number))

        # Cleans up database of employees' photographs
        shutil.rmtree("dataset")
        os.mkdir("dataset")

        return face_number

    # function to get the images and label data
    def get_images_and_labels(self, path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]

        face_samples = []
        ids = []

        for image_path in image_paths:
            PIL_img = Image.open(image_path).convert('L')  # convert it to greyscale
            img_numpy = np.array(PIL_img, 'uint8')

            identificator = int(os.path.split(image_path)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y: y+h, x: x+w])
                ids.append(identificator)

        return face_samples, ids
