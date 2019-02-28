# Real Time Face Recogition
# ==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc
# ==> LBPH computed model (trained faces) should be on trainer/ dir

import cv2
import time
import threading
from tkinter import *
from scripts.database_connection import Connection


class Recogniser:
    def __init__(self):
        self.__init_UI__()
        self.start_recognising_btn.pack(side="left")
        self.window.mainloop()

    def start_threads(self):
        ids = []
        with open("scripts/config.conf", "r") as f:
            lines = f.readlines()
            for line in lines:
                ids.append(line.split("=")[1].encode("cp1251").decode("UTF-8"))

        threading.Thread(target=self.recognise, args=(0, ids[0])).start()
        threading.Thread(target=self.recognise, args=(1, ids[1])).start()

    def __init_UI__(self):
        self.window = Tk()
        self.window.geometry("1270x950+0+0")
        self.window.wm_title("Распознавание сотрудников")

        self.start_recognising_btn = Button(self.window, text="Начать распознавание",
                                            width=25, height=3,
                                            font="arial 14",
                                            command=threading.Thread(target=self.start_threads).start)

        self.exit_btn = Button(self.window, text="Закончить распознавание",
                               width=25, height=3,
                               font="arial 14", command=self.window.destroy)

    def recognise(self, cam_id, id):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

        conn, cursor = Connection.connect("WorkAttendance")

        # Initialize and start real-time video capture
        cam = cv2.VideoCapture(cam_id)
        cam.set(5, 1000)  # set video height
        cam.set(5, 1900)  # set video width

        # Define min window size to be recognized as a face
        min_w = 10
        min_h = 10

        self.exit_btn.pack(side="right")

        print("[INFO] Starting to recognise")
        try:
            while True:
                ids = {}
                for count in range(60):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(int(min_w), int(min_h)))

                    for (x, y, w, h) in faces:
                        identificator, confidence = recognizer.predict(gray[y: y + h, x: x + w])

                        # Check if confidence is less then 60 ==> "0" is perfect match
                        if confidence < 60:  # experiment! 50-70
                            print(confidence)
                            # confidence = "{0}%".format(round(100 - confidence))
                            count = ids.get(identificator)
                            if count is not None:
                                ids.update({identificator: count + 1})
                            else:
                                ids.update({identificator: 1})

                for key in ids.keys():
                    if ids.get(key) > 3:
                        cursor.execute("""INSERT INTO
                                       WorkAttendance.dbo.LOGs(Дата_Время, Табельный_номер, ID_камеры)
                                       VALUES(?,?,?)""", [time.strftime("%Y-%m-%d %H:%M:%S"), str(key), id])

                        person = cursor.execute("""SELECT Фамилия, Имя, Отчество 
                                                FROM WorkAttendance.dbo.FIO_Tabels
                                                WHERE Табельный_номер=""" + str(key)).fetchone()

                        cursor.commit()

                        lbl = Label(self.window, text=" ".join([person[0], person[1], person[2]]),
                                    width=50, height=4,
                                    font="arial 24")
                        lbl.pack(side="top")
                        lbl.after(5000, lambda: lbl.destroy())

                        self.window.update()

        except Exception as e:
            self.window.destroy()
            cam.release()
            cv2.destroyAllWindows()
        finally:
            # Do a bit of cleanup
            print("[INFO] Exiting Program and cleanup stuff")
            cam.release()
            cv2.destroyAllWindows()
            cursor.close()
            conn.close()





if __name__ == "__main__":
    Recogniser()
