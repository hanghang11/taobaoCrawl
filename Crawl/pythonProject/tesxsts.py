import pyperclip as pc
# pc.copy("I love Programming")
from tkinter import *

def showPopoutMenu(w, menu):
    def popout(event):
        menu.post(event.x + w.winfo_rootx(), event.y + w.winfo_rooty())
        w.update()

    w.bind('<Button-3>', popout)


w = Tk()
w.title('Pop-Out Menu')

lab = Label(text='I am a Label widget with right-click menu! ')
lab.place(x=0, y=0)
menu = Menu(w)
menu.add_cascade(label='功能一')
menu.add_cascade(label='功能二')
showPopoutMenu(lab, menu)

w.mainloop()