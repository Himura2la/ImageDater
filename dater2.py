#! python3
# -*- coding: utf-8 -*-
import os
import sys
import tkinter
from tkinter import ttk, messagebox

from PIL import Image, ImageDraw, ImageFont # pip install Pillow
import piexif # pip install piexif

префикс_имён_файлов = 'D_'
размер_шрифта = 100
отступ_слева = 20
отступ_снизу = 20
шрифт = ImageFont.truetype('%WINDIR%\\Fonts\\arial.ttf', размер_шрифта)
цвет_шрифта = (255, 255, 255)
прозрачность_подложки = 30  # Процентов
цвет_подложки = (0, 0, 0, round(прозрачность_подложки/100*255))


class Приложение(ttk.Frame):
    def __init__(self, пути_к_картинкам, master=None):
        super().__init__(master)
        if not пути_к_картинкам:
            master.withdraw()
            messagebox.showerror('Нет картинок :(', 'Не нашёл изображений. Брось мышкой нужные картинки на иконку программы. Запускать двойным кликом не нужно, это так не работает...')
            master.destroy()
            return

        self.master = master
        self.master.title("Проставлялка дат")
        self.даты = {}

        for картинка in пути_к_картинкам:
            self.строка = ttk.Frame(self)
            self.даты[картинка] = tkinter.StringVar(self.строка, value=прочитать_дату(картинка))

            self.надпись_файл = tkinter.Label(self.строка, text=картинка)
            self.надпись_файл.pack(side='left')
            self.поле_даты = ttk.Entry(self.строка, textvariable=self.даты[картинка])
            self.поле_даты.pack(side='right', fill='x', expand=True)

            self.строка.pack(side='top', fill="x")
        
        self.кнопка_проставить = ttk.Button(self, text="Проставить всем даты", command=self.проставить_всем)
        self.кнопка_проставить.pack(fill='both', expand=True)
        self.pack(fill='both', expand=True)

    def проставить_всем(self):
        for картинка, поле_даты in self.даты.items():
            дата = поле_даты.get()
            проставить_дату(картинка, дата)
        self.master.destroy()
        return


def прочитать_дату(путь_к_файлу):
    картинка = Image.open(путь_к_файлу).convert('RGB')
    try:
        exif = piexif.load(картинка.info['exif'])
        дата_съемки = exif['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
        дата, время = дата_съемки.split(' ', 1)
        год, месяц, число = дата.split(':', 3)
        return f"{число}.{месяц}.{год[2:]} {время}"
    except KeyError:
        return "бездато"


def проставить_дату(путь_к_файлу, дата_съемки):
    картинка = Image.open(путь_к_файлу).convert('RGB')
    ширина, высота = картинка.size
    draw = ImageDraw.Draw(картинка, 'RGBA')

    text_width, text_height = draw.textsize(дата_съемки, шрифт)
    draw.rectangle([отступ_снизу, высота - text_height - отступ_снизу, text_width + отступ_слева, высота - отступ_снизу], цвет_подложки)

    draw.text((отступ_слева, высота - text_height - round(размер_шрифта / 10) - отступ_снизу), дата_съемки, цвет_шрифта, шрифт)

    folder, filename = os.path.split(путь_к_файлу)
    картинка.save(os.path.join(folder, префикс_имён_файлов + filename))


# Здесь начинается выполнение программы.

root = tkinter.Tk()  # Создаем управлялку оконной подсистемой
app = Приложение(sys.argv[1:], master=root)  # Создаем приложение, описанное выше
app.mainloop()  # Запускаем приложение
