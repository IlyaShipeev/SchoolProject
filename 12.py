import tkinter
from tkinter import filedialog, messagebox, scrolledtext
import cv2
from PIL import Image, ImageTk
from pytesseract import pytesseract

pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'


class Program:
    def __init__(self):
        # Главное окно
        self.main_window = tkinter.Tk()
        # Имя главного окна
        self.main_window.title("Text Recognition App ")
        # Возможность растяжения по оси x и y
        self.main_window.resizable(0, 0)
        self.main_window.protocol("WM_DELETE_WINDOW", self.closing_app)
        # Рамка, на которой будет размещен холст с изображением
        self.ImageFrame = tkinter.Frame(self.main_window,
                                        width=600, height=700)
        # Размещение рамки
        self.ImageFrame.grid(row=0, column=0)

        self.text = None
        # Язык по умолчанию
        self.lang = "rus"

        self.photo = None
        self.canvas_image = None
        self.path = None

        # Холст, на котором будет располагаться изображение
        self.canvas = tkinter.Canvas(self.ImageFrame, height=780, width=600)
        # Полоса прокрутки по оси x
        self.scroll_x = tkinter.Scrollbar(self.ImageFrame,
                                          orient="horizontal", command=self.canvas.xview)
        # Размещение полосы прокрутки по оси x
        self.scroll_x.grid(row=1, column=0, sticky="we")
        # Полоса прокрутки по оси y
        self.scroll_y = tkinter.Scrollbar(self.ImageFrame,
                                          orient="vertical", command=self.canvas.yview)
        # Размещение полосы прокрутки по оси y
        self.scroll_y.grid(row=0, column=2, sticky="ns")
        # Размещение холста
        self.canvas.grid(row=0, column=0)

        # Текст
        self.text_field = scrolledtext.ScrolledText(
            master=self.main_window, width=60,
            height=50, wrap="word", font=("Verdana", 10))
        self.text_field.grid(row=0, column=2)

        # Файл
        self.main_menu = tkinter.Menu(master=self.main_window)
        self.file_menu = tkinter.Menu(master=self.main_menu, tearoff=0)
        self.file_menu.add_command(label="Открыть", command=self.show_image)

        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)

        # Подвязывание к панели меню
        self.lang_menu = tkinter.Menu(master=self.main_menu, tearoff=0)

        # Переменная связывающая кнопки, имеющая два значения
        self.lang_var = tkinter.BooleanVar()
        # Кнопки, принимающие одно значением
        self.lang_menu.add_radiobutton(
            label="Русский", command=self.set_russian_lang, variable=self.lang_var)
        self.lang_menu.add_radiobutton(
            label="Английский", command=self.set_english_lang, variable=self.lang_var)


        self.main_menu.add_cascade(label="Язык", menu=self.lang_menu)

        self.main_menu.add_command(label="Получить текст",
                                   command=self.insert_text)
        self.main_window.config(menu=self.main_menu)

        self.main_window.mainloop()

    def show_image(self):
        self.path = filedialog.askopenfilename(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        img = Image.open(self.path)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=0, column=0)

    def insert_text(self):
        # Переменная с изображением
        cv2_image = cv2.imread(self.path)
        # Фильтр
        gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        # Определение области с текстом
        changed_img = cv2.adaptiveThreshold(gray,
                                            255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 30)
        # Получение символов из определенного языка
        self.text = pytesseract.image_to_string(changed_img, lang=self.lang)[:-1]
        # Очистка текстового поля
        self.text_field.delete('1.0', tkinter.END)
        # Вывод текста
        self.text_field.insert(1.0, self.text)

    def set_english_lang(self):
        self.lang = "eng"
        return self.lang

    def set_russian_lang(self):
        self.lang = "rus"
        return self.lang

    def closing_app(self):
        if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
            self.main_window.destroy()


if __name__ == '__main__':
    Program()
