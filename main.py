import tkinter
from tkinter import filedialog, messagebox, scrolledtext
import cv2
from PIL import Image, ImageTk
from pytesseract import pytesseract

pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'


class Program:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title("Text Recognition App ")
        self.main_window.resizable(0, 0)

        self.main_window.protocol("WM_DELETE_WINDOW", self.closing_app)

        self.ImageFrame = tkinter.Frame(self.main_window,
                                        width=600, height=700, bg='gray')
        self.ImageFrame.grid(row=0, column=0)
        self.text = None
        self.lang = "rus"
        self.photo = None
        self.canvas_image = None
        self.path = None

        self.canvas = tkinter.Canvas(self.ImageFrame, height=780, width=600, bg="white")
        self.scroll_x = tkinter.Scrollbar(
            self.ImageFrame, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky="we")

        self.scroll_y = tkinter.Scrollbar(
            self.ImageFrame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=2, sticky="ns")

        self.canvas.grid(row=0, column=0)

        self.text_field = scrolledtext.ScrolledText(
            master=self.main_window, width=60, height=50, wrap="word", font=("Verdana", 10))
        self.text_field.grid(row=0, column=2)

        # Панель меню
        self.main_menu = tkinter.Menu(master=self.main_window)

        # Подвязывание к панели меню
        self.file_menu = tkinter.Menu(master=self.main_menu, tearoff=0)
        # Пункт меню "Открыть"
        self.file_menu.add_command(label="Открыть")
        # Выпадающее меню "Файл"
        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        # Меню "Язык"
        self.lang_menu = tkinter.Menu(master=self.main_menu, tearoff=0)
        self.rus_var = tkinter.BooleanVar(value=1)
        self.eng_var = tkinter.BooleanVar(value=0)

        self.lang_menu.add_checkbutton(
            label="Русский", variable=self.rus_var, command=self.set_russian_lang, onvalue=1)
        self.lang_menu.add_checkbutton(
            label="Английский", command=self.set_english_lang, variable=self.eng_var, onvalue=1)
        # Выпадающее меню "Язык"
        self.main_menu.add_cascade(label="Язык", menu=self.lang_menu)
        self.main_menu.add_command(label="Получить текст", command=self.insert_text)
        # Разместить панель меню
        self.main_window.config(menu=self.main_menu)
        self.main_window.mainloop()

    # Функция отображения изображения
    def show_image(self):
        # Путь до файла
        self.path = filedialog.askopenfilename(
            filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        # Получение изображения
        img = Image.open(self.path)
        self.photo = ImageTk.PhotoImage(img)
        # Отображение на холсте
        self.canvas_image = self.canvas.create_image(
            0, 0, anchor='nw', image=self.photo)
        self.canvas.grid(row=0, column=0)

    def insert_text(self):
        cv2_image = cv2.imread(self.path)
        gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        changed_img = cv2.adaptiveThreshold(gray,
                                            255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 30)
        self.text = pytesseract.image_to_string(changed_img, lang=self.lang)
        self.text = self.text.replace('', '')

        self.text_field.delete('1.0', tkinter.END)
        self.text_field.insert(1.0, self.text)

    def set_english_lang(self):
        self.lang = "eng"
        self.eng_var.set(value=1)
        self.rus_var.set(value=0)

    def set_russian_lang(self):
        self.lang = "rus"
        self.rus_var.set(value=1)
        self.eng_var.set(value=0)

    def closing_app(self):
        if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
            self.main_window.destroy()


if __name__ == '__main__':
    Program()
