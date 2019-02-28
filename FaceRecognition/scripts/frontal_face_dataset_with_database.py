# Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
# ==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
# ==> Each face will have a unique numeric integer ID as 1, 2, 3, etc


import cv2
from scripts.database_connection import Connection
from tkinter import *


class Photographer:
    def __init__(self, f, i, o="", face_id=None):
        self._face_id = face_id
        _to_database = [self._face_id, f, i, o]

        conn, cursor = Connection.connect("WorkAttendance")
        print (conn, cursor)
        try:
            cursor.execute("""INSERT INTO
                            WorkAttendance.dbo.FIO_Tabels(Табельный_номер, Фамилия, Имя, Отчество)
                            VALUES(?,?,?,?)""", _to_database)
            cursor.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("[Ошибка!] " + str(e))
            window = Tk()
            window.wm_title("Ошибка!")
            Label(window, text=str(e),
                  font="arial 14").grid(row=0, column=0)
            window.mainloop()
            cv2.destroyAllWindows()

    def make_photo_set(self):
        cam = cv2.VideoCapture(0)
        cam.set(5, 1900)  # set video width
        cam.set(5, 1000)  # set video height

        face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
        eye_detector = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')

        print("[INFO] Инициализация захвата лица. " +
              "\nСмотрите в камеру и равномерно, медленно поворачивайте лицо по сторонам.")

        # Initialize individual sampling face count
        count = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(20, 20)
            )

            for (x, y, w, h) in faces:
                face_saved = False
                count += 1
                roi_gray = gray[y:y+h, x:x+w]

                eyes = eye_detector.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(5, 5)
                )

                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.imshow('video', img)
                    if not face_saved:
                        # Save the captured image into the dataset folder
                        cv2.imwrite("dataset/User." + str(self._face_id) + '.' + str(count) + ".jpg",
                                    gray[y:y+h, x:x+w])
                        face_saved = True

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 150:  # Take 150 face sample and stop video
                break

        # Do a bit of clean up
        print("[INFO] Exiting Program and cleaning up stuff")
        cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    face_id = input("Введите табельный номер работика и нажмите <Return> ==> ")
    f, i, o = input("Введите ФИО ==> ").split(" ")
    Photographer(f, i, o, face_id).make_photo_set()
else:
    "Вы исользуете frontal_face_dataset_with_database_with_control как библиотеку."
