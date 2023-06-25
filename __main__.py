from tkinter import *

root = Tk()
root.title('Производственная практика')
root.minsize(300, 200)

btn1 = Button(root, text='Конвертация таблиц', command=lambda: __import__('convert'))
btn2 = Button(root, text='Выбор базы данных', command=lambda: __import__('dbselect'))

btn1.place(anchor='center', relx=0.5, rely=0.40)
btn2.place(anchor='center', relx=0.5, rely=0.60)

root.mainloop()
