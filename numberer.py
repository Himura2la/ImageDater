#! python3
# -*- coding: utf-8 -*-
import os
import sys
import datetime
import tkinter
from tkinter import ttk
import win32clipboard

from PIL import Image, ImageDraw, ImageFont

путь_к_билету = r"ticket.jpg"
куда_складывать_билеты = r"Билеты"
размер_билета = (2425, 1087)

шрифт = ImageFont.truetype('%WINDIR%\\Fonts\\arial.ttf', 80)
цвет_шрифта = (0, 0, 0)
положение_x, положение_y = (90, 485)

if not os.path.isdir(куда_складывать_билеты):
    os.makedirs(куда_складывать_билеты)

class Приложение(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Проставлятель номеров билетов")

        self.поле_кода = ttk.Entry(master, font="sans-serif 44 bold")
        self.кнопка = ttk.Button(master, text=f"Продать билет", command=self.продать)

        self.поле_кода.pack(fill='x')
        self.кнопка.pack(fill='x')
        self.pack(fill='both', expand=True)

        clipboard = master.clipboard_get()
        if clipboard:
            self.поле_кода.insert(0, clipboard)

    def продать(self):
        код_билета = self.поле_кода.get().strip()
        изображение_билета = Image.open(путь_к_билету).convert('RGB')
        изображение_текста = Image.new('RGBA', шрифт.getsize(код_билета))
        холст_текста = ImageDraw.Draw(изображение_текста)
        холст_текста.text((0, 0), код_билета, цвет_шрифта, шрифт)
        изображение_текста = изображение_текста.rotate(90,  expand=1)
        sx, sy = изображение_текста.size
        положение_y_от_цента = положение_y - sy // 2
        изображение_билета.paste(изображение_текста, (положение_x, положение_y_от_цента, положение_x + sx, положение_y_от_цента + sy), изображение_текста)
        имя_файла = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S_") + код_билета + ".jpg"
        изображение_билета.save(os.path.join(куда_складывать_билеты, имя_файла))
        self.quit()

# Здесь начинается выполнение программы.

root = tkinter.Tk()  # Создаем оконную подсистему
app = Приложение(root)  # Создаем приложение, описанное выше
app.mainloop()  # Запускаем приложение
