from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.geometry("500x200")

mbtn = Menubutton(root, text="Options", relief=RAISED)
mbtn.pack()
mbtn.menu = Menu(mbtn, tearoff = 0)
mbtn["menu"] = mbtn.menu

photo = ImageTk.PhotoImage(Image.open('./img/amostra1.png'))

l = Label(image=photo).pack()
mbtn.menu.add_checkbutton(label=l)
mbtn.menu.add_checkbutton(label=l)
mbtn.menu.add_checkbutton(label=l)


root.mainloop()
    