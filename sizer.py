#! python3
# -*- coding: utf-8 -*-
import os
import tkinter
from tkinter import ttk

import sys
from PIL import Image

ширина_картинки = 400
сжатие_картинки = 50
префикс_имён_файлов = 'S_'


class Приложение(ttk.Frame):
    def __init__(self, image_paths, master=None):
        super().__init__(master)
        self.пути_к_картинкам = image_paths
        self.master.title("Уменьшалка Картинок")

        # Делаем кнопки
        self.кнопка_уменьшить = ttk.Button(self, text=f"Ширину на {ширина_картинки}px", command=self.уменьшить)
        self.кнопка_сжать = ttk.Button(self, text=f"Сжатие на {сжатие_картинки}%", command=self.сжать)

        # Раскладываем кнопки
        self.кнопка_уменьшить.pack(fill='x')
        self.кнопка_сжать.pack(fill='x')
        self.pack(fill='both', expand=True)

    def уменьшить(self):
        for путь_к_файлу in self.пути_к_картинкам:
            картинка = Image.open(путь_к_файлу).convert('RGB')
            ширина, высота = картинка.size

            if ширина > 400:
                высота_картинки = round(ширина_картинки * высота / ширина)
                картинка = картинка.resize((ширина_картинки, высота_картинки), Image.ANTIALIAS)

            папка, имя_файла = os.path.split(путь_к_файлу)
            картинка.save(os.path.join(папка, префикс_имён_файлов + имя_файла))
        self.quit()

    def сжать(self):
        for путь_к_файлу in self.пути_к_картинкам:
            img = Image.open(путь_к_файлу).convert('RGB')
            папка, имя_файла = os.path.split(путь_к_файлу)
            img.save(os.path.join(папка, префикс_имён_файлов + имя_файла), format='JPEG', quality=сжатие_картинки)
        self.quit()

# Здесь начинается выполнение программы.

if len(sys.argv) < 2:
    print('Не нашёл изображений. Надо передать список файлов в качестве аргументов.\n'
          'Если ты из под венды, просто брось мышкой нужные файлы на это приложение.\n\n'
          'Топи Enter, чтобы выйти и попробывать еще раз.')
    input()
    exit()

пути_к_файлам = sys.argv[1:]  # Читаем что было брошено на скрипт

root = tkinter.Tk()  # Создаем управлялку оконной подсистемой
app = Приложение(пути_к_файлам, master=root)  # Создаем приложение, описанное выше
app.mainloop()  # Запускаем приложение
