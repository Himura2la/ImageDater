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


class Application(ttk.Frame):
    def __init__(self, image_paths, master=None):
        super().__init__(master)
        self.image_paths = image_paths
        self.pack(fill='both', expand=True)

        self.master.title("Уменьшалка Картинок")

        self.frame = ttk.Frame(self)

        self.scale_btn = ttk.Button(self.frame, text=f"Ширину на {ширина_картинки}px", command=self.scale)
        self.compress_btn = ttk.Button(self.frame, text=f"Сжатие на {сжатие_картинки}%", command=self.compress)

        self.scale_btn.pack(fill='x')
        self.compress_btn.pack(fill='x')

        self.frame.pack(fill='x')

    def scale(self):
        for path in self.image_paths:
            img = Image.open(path).convert('RGB')
            width, height = img.size

            if width > 400:
                высота_картинки = round(ширина_картинки * height / width)
                img = img.resize((ширина_картинки, высота_картинки), Image.ANTIALIAS)

            folder, filename = os.path.split(path)
            img.save(os.path.join(folder, префикс_имён_файлов + filename))
        self.quit()

    def compress(self):
        for path in self.image_paths:
            img = Image.open(path).convert('RGB')
            folder, filename = os.path.split(path)
            img.save(os.path.join(folder, префикс_имён_файлов + filename), format='JPEG', quality=сжатие_картинки)
        self.quit()

if len(sys.argv) < 2:
    print('Не нашёл изображений. Надо передать список файлов в качестве аргументов.\n'
          'Если ты из под венды, просто брось мышкой нужные файлы на это приложение.\n\n'
          'Топи Enter, чтобы выйти и попробывать еще раз.')
    input()
    exit()


paths = sys.argv[1:]

root = tkinter.Tk()
app = Application(paths, master=root)
app.mainloop()
