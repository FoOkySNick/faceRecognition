from multiprocessing import Process
from tkinter import *
from scripts.frontal_face_dataset_with_database import Photographer
from scripts.frontal_faces_training_with_reading_and_cleanup import Trainer
from scripts.frontal_face_recognition_with_GUI_and_database import Recogniser


class Main:
    def __init__(self):
        self.__initUI__()

    def __initUI__(self):
        self.root = Tk()
        self.root.wm_title("Проверка присутствия работников")
        self.root.geometry("1270x950+0+0")

        self.__init_PhotosUI__()
        self.__init_RecogniserUI__()

        photos_btn = Button(self.root, text="Начать фотографирование",
                               width=25, height=3,
                               font="arial 14", command=self.photos_btn_pressed)
        photos_btn.grid(row=1, column=0)

        st_lbl1 = Label(self.root, text="Создает множество фотографий лица",
                        width=38, height=3,
                        font="arial 14")
        st_lbl1.grid(row=0, column=0)

        trainer_btn = Button(self.root, text="Тренировка распознавателя",
                      width=25, height=3,
                      font="arial 14", command=self.trainer_btn_pressed)
        trainer_btn.grid(row=1, column=1)

        st_lbl2 = Label(self.root, text="Обучение продлится некоторое время",
                        width=38, height=3,
                        font="arial 14")
        st_lbl2.grid(row=0, column=1)

        recogniser_btn = Button(self.root, text="Распознавание",
                      width=25, height=3,
                      font="arial 14", command=self.recogniser_btn_pressed)
        recogniser_btn.grid(row=1, column=2)

        st_lbl2 = Label(self.root, text="Начало работы программы по распознаванию",
                        width=38, height=3,
                        font="arial 14")
        st_lbl2.grid(row=0, column=2)

        self.root.mainloop()

    def __init_PhotosUI__(self):
        self.photos_tabel_lbl = Label(self.root, text="Введите табельный номер сотрудника.",
                                      width=38, height=3,
                                      font="arial 14")
        self.photos_ok_btn = Button(self.root, text="Подтвердить",
                                    font="arial 14", command=self.photos_ok_btn_pressed)
        self.entry_FIO = Entry(self.root, bd=5)
        self.photos_FIO_lbl = Label(self.root, text="Введите ФИО.",
                                    width=38, height=3,
                                    font="arial 14")
        self.entry_tabel_number = Entry(self.root, bd=5)
        self.photos_look_info_lbl = Label(self.root, text="Смотрите в камеру." +
                                                          "\nМедленно поворачивайте лицо " +
                                                          "\nиз стороны в сторорну.",
                                          width=38, height=5,
                                          font="arial 14")
        self.photos_exit_lbl = Label(self.root, text=" Выход из приложения. Освобождение ресурсов.",
                                     width=38, height=3,
                                     font="arial 14")

    def __init_RecogniserUI__(self):
        self.recogniser_start_lbl = Label(self.root, text="Управление передано распознавателю",
                                          width=38, height=3,
                                          font="arial 14")
        self.recogniser_exit_btn = Button(self.root, text="Завершить",
                                          font="arial 14", command=self.recogniser_exit_btn_pressed)
        self.recogniser_exit_lbl = Label(self.root, text="Выход из приложения. Освобождение ресурсов.",
                                         width=38, height=3,
                                         font="arial 14")

    def photos_btn_pressed(self):
        self.photos_tabel_lbl.grid(row=2, column=0)
        self.entry_tabel_number.grid(row=3, column=0)
        self.photos_FIO_lbl.grid(row=4, column=0)
        self.entry_FIO.grid(row=5, column=0)
        self.photos_ok_btn.grid(row=6, column=0)

    def photos_ok_btn_pressed(self):
        fio = self.entry_FIO.get().split(" ")
        face_id = self.entry_tabel_number.get()

        self.photos_FIO_lbl.grid_remove()
        self.entry_FIO.grid_remove()
        self.photos_ok_btn.grid_remove()
        self.entry_tabel_number.grid_remove()
        self.photos_tabel_lbl.grid_remove()

        self.photos_look_info_lbl.grid(row=2, column=0)
        self.photos_look_info_lbl.after(3000, lambda: self.photos_look_info_lbl.grid_remove())

        self.root.update()

        Photographer(face_id=face_id, *fio).make_photo_set()

        self.photos_exit_lbl.grid(row=2, column=0)
        self.photos_exit_lbl.after(3000, lambda: self.photos_exit_lbl.grid_remove())

        self.root.update()

    def trainer_btn_pressed(self):
        trained_faces_number = Trainer().train()

        trainer_exit_lbl = Label(self.root, text="Выход из программы. Освобождение ресурсов." +
                                                 "\n" + str(trained_faces_number) + " лиц изучено",
                                 width=38, height=4,
                                 font="arial 14")
        trainer_exit_lbl.grid(row=2, column=1)
        self.root.update()
        trainer_exit_lbl.after(3000, lambda: trainer_exit_lbl.grid_remove())

    def recogniser_btn_pressed(self):
        self.recogniser_start_lbl.grid(row=2, column=2)
        self.recogniser_exit_btn.grid(row=3, column=2)

        self.root.update()

        self.recogniser_process = Process(target=Recogniser)
        self.recogniser_process.start()

    def recogniser_exit_btn_pressed(self):
        self.recogniser_start_lbl.grid_remove()
        self.recogniser_exit_btn.grid_remove()

        self.recogniser_process.terminate()

        self.recogniser_exit_lbl.grid(row=2, column=2)
        self.recogniser_exit_lbl.after(3000, lambda: self.recogniser_exit_lbl.grid_remove())

        self.root.update()


if __name__ == "__main__":
    Main()
