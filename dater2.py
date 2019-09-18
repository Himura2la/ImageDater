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
        self.exif = {}

        for картинка in пути_к_картинкам:
            self.строка = ttk.Frame(self)
            self.exif[картинка] = прочитать_EXIF(картинка)
            дата = self.exif[картинка]["дата"] if self.exif[картинка] else "пусто"
            self.даты[картинка] = tkinter.StringVar(self.строка, value=дата)

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
            проставить_дату(картинка, дата, self.exif[картинка]["ориентация"])
        self.master.destroy()
        return


def прочитать_EXIF(путь_к_файлу):
    картинка = Image.open(путь_к_файлу).convert('RGB')
    try:
        exif = piexif.load(картинка.info['exif'])
        дата_съемки = exif['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
        дата, время = дата_съемки.split(' ', 1)
        год, месяц, число = дата.split(':', 3)
        ориентация = exif["0th"][piexif.ImageIFD.Orientation]
        return {
            "дата": f"{число}.{месяц}.{год[2:]} {время}",
            "ориентация": ориентация
        }
    except KeyError:
        return None


def проставить_дату(путь_к_файлу, дата_съемки, ориентация):
    картинка = Image.open(путь_к_файлу).convert('RGB')

    if ориентация == 2:
        картинка = картинка.transpose(Image.FLIP_LEFT_RIGHT)
    elif ориентация == 3:
        картинка = картинка.rotate(180)
    elif ориентация == 4:
        картинка = картинка.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    elif ориентация == 5:
        картинка = картинка.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    elif ориентация == 6:
        картинка = картинка.rotate(-90, expand=True)
    elif ориентация == 7:
        картинка = картинка.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    elif ориентация == 8:
        картинка = картинка.rotate(90, expand=True)

    ширина, высота = картинка.size
    разрешение = (ширина**2 + высота**2)**0.5
    относительный_размер_шрифта = int(размер_шрифта * разрешение / 5000)
    шрифт = ImageFont.truetype('%WINDIR%\\Fonts\\arial.ttf', относительный_размер_шрифта)

    относительный_отступ_снизу = int(отступ_снизу * разрешение / 5000)
    относительный_отступ_слева = int(отступ_слева * разрешение / 5000)
    
    draw = ImageDraw.Draw(картинка, 'RGBA')

    text_width, text_height = draw.textsize(дата_съемки, шрифт)
    draw.rectangle([относительный_отступ_снизу,
                    высота - text_height - относительный_отступ_снизу,
                    text_width + относительный_отступ_слева,
                    высота - относительный_отступ_снизу - 1],
                   цвет_подложки)

    draw.text((относительный_отступ_слева,
               высота - text_height - round(относительный_размер_шрифта / 10) - относительный_отступ_снизу),
              дата_съемки,
              цвет_шрифта,
              шрифт)

    folder, filename = os.path.split(путь_к_файлу)
    картинка.save(os.path.join(folder, префикс_имён_файлов + filename))


# Здесь начинается выполнение программы.

root = tkinter.Tk()  # Создаем управлялку оконной подсистемой
app = Приложение(sys.argv[1:], master=root)  # Создаем приложение, описанное выше
app.mainloop()  # Запускаем приложение
