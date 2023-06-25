import os
import sys
import shutil
from tkinter import *
from tkinter.messagebox import *

def action(city, year):
    if os.path.isdir('PFRNET'):
        shutil.rmtree('PFRNET')
    if os.path.isdir('PFRSOFT'):
        shutil.rmtree('PFRSOFT')
    
    try:
        shutil.copytree(f'PF_{city}{year}', 'PFRNET')
    except:
        showerror('Ошибка', f'Папка PF_{city}{year} не существует')
        return

    try:
        shutil.copytree(f'SOFT_{city}{year}', 'PFRSOFT')
    except:
        showerror('Ошибка', f'Папка SOFT_{city}{year} не существует')
        return

root = Tk()

iv1997 = Button(root, text='Ивантеевка 1997', command=lambda: action('IV', 1997))
iv2000 = Button(root, text='Ивантеевка 2000', command=lambda: action('IV', 2000))

kr1997 = Button(root, text='Красноармейск 1997', command=lambda: action('KR', 1997))
kr2000 = Button(root, text='Красноармейск 2000', command=lambda: action('KR', 2000))

pu1997 = Button(root, text='Пушкино 1997', command=lambda: action('PU', 1997))
pu2000 = Button(root, text='Пушкино 2000', command=lambda: action('PU', 2000))

iv1997.pack()
iv2000.pack()
kr1997.pack()
kr2000.pack()
pu1997.pack()
pu2000.pack()

root.mainloop()