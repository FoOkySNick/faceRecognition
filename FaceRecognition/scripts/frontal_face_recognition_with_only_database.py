# Real Time Face Recogition
# ==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc
# ==> LBPH computed model (trained faces) should be on trainer/ dir

import cv2
import time
import threading
from tkinter import Tk, Label
from scripts.database_connection import Connection


class Recogniser:
    def __init__(self):
        ids = []
        with open("scripts/config.conf", "r") as f:
            lines = f.readlines()
            for line in lines:
                ids.append(line.split("=")[1].encode("cp1251").decode("UTF-8"))

        threading.Thread(target=self.recognise, args=(0, ids[0])).start()
        threading.Thread(target=self.recognise, args=(1, ids[1])).start()

    def recognise(self, cam_id, id):
        # Initialize and start real-time video capture
        cam = cv2.VideoCapture(cam_id )
        cam.set(6, 1280)  # set video width
        cam.set(8, 960)  # set video height

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

        conn, cursor = Connection.connect("WorkAttendance")

        # Define min window size to be recognized as a face
        min_w = 20
        min_h = 20

        print("[INFO] Starting to recognise")
        try:
            while True:
                ids = {}
                for count in range(90):
                    ret, img = cam.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(min_w, min_h)
                    )

                    for (x, y, w, h) in faces:
                        identificator, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                        # Check if confidence is less then 100 ==> "0" is perfect match
                        if confidence < 60:  # experiment! 50-70
                            count = ids.get(identificator)
                            if count is not None:
                                ids.update({identificator: count + 1})
                            else:
                                ids.update({identificator: 1})

                for key in ids.keys():
                    if ids.get(key) > 5:
                        cursor.execute("""INSERT INTO
                            WorkAttendance.dbo.LOGs(Дата_Время, Табельный_номер, ID_камеры)
                            VALUES(?,?,?)""", [time.strftime("%Y-%m-%d %H:%M:%S"),  str(key), id])
                        cursor.commit()
        except Exception as e:
            print("[Ошибка!] " + str(e))
            window = Tk()
            window.wm_title("Ошибка!")
            Label(window, text=str(e),
                  font="arial 14").grid(row=0, column=0)
            window.mainloop()
            cv2.destroyAllWindows() # Release resources
            try:
                cam.release()
            except Exception:
                pass
        finally:
            # Do a bit of cleanup
            print("[INFO] Exiting Program and cleanup stuff")
            try:
                cam.release()
                cursor.close()
                conn.close()
            except Exception:
                pass


if __name__ == "__main__":
    Recogniser()
else:
    print("Вы используете database_connection как библиотеку")