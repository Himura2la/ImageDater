#!python3
# -*- coding: utf-8 -*-

# pip install Pillow piexif

from PIL import Image, ImageDraw, ImageFont
import piexif
import sys
import os

префикс_имён_файлов = 'D_'
ширина_картинки = 400
размер_шрифта = 25
цвет_шрифта = (255, 255, 255)
прозрачность_подложки = 30  # Процентов
цвет_подложки = (0, 0, 0, round(прозрачность_подложки/100*255))

шрифт = ImageFont.truetype('%WINDIR%\\Fonts\\arial.ttf', размер_шрифта)

# --------------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print('Не нашёл изображений. Надо передать список файлов в качестве аргументов.\n'
          'Если ты из под венды, просто брось мышкой нужные файлы на это приложение.\n\n'
          'Топи Enter, чтобы выйти и попробывать еще раз.')
    input()
    exit()

image_paths = sys.argv[1:]

for path in image_paths:
    img = Image.open(path).convert('RGB')
    width, height = img.size

    if width > 400:
        высота_картинки = round(ширина_картинки * height / width)
        img = img.resize((ширина_картинки, высота_картинки), Image.ANTIALIAS)
        width, height = ширина_картинки, высота_картинки
    try:
        exif = piexif.load(img.info['exif'])
        дата_съемки = exif['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
        дата, время = дата_съемки.split(' ', 1)
        год, месяц, число = дата.split(':', 3)
        дата_съемки = f"{число}/{месяц}/{год[2:]} {время}"
    except KeyError:
        дата_съемки = input(f'У {path} нет даты. Введи ее в таком формате: 31/12/99 23:59:59')

    draw = ImageDraw.Draw(img, 'RGBA')

    text_width, text_height = draw.textsize(дата_съемки, шрифт)
    draw.rectangle([0, height-text_height, text_width, height], цвет_подложки)

    отступ_снизу = round(размер_шрифта / 8)
    draw.text((1, height - text_height - отступ_снизу), дата_съемки, цвет_шрифта, шрифт)

    folder, filename = os.path.split(path)
    img.save(os.path.join(folder, префикс_имён_файлов + filename))
