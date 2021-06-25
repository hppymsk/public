from tkinter import *
from tkinter.ttk import *

#Setup the window
window = Tk()
window.title("Hello World")
window.geometry('350x200')

#Clickdown list
combo = Combobox(window)
combo['values'] =  (1, 2, 3, 4, 5, "Text")
combo.current(1)
combo.grid(column=0, row=0)

#Checkbox
chk_state = BooleanVar()
chk_state.set(True)
chk = Checkbutton(window, text='Choose', var=chk_state)
chk.grid(column=0, row=1)

#Spinbox
var = IntVar()
var.set(36)
spin = Spinbox(window, from_=4, to=300, width=4, textvariable=var)
spin.grid(column=0, row=4)
#Radio buttons
selected = IntVar()
rad1 = Radiobutton(window, text='First', value=1, variable=selected)
rad2 = Radiobutton(window, text='Second', value=2, variable=selected)
rad3 = Radiobutton(window, text='Third', value=3, variable=selected)
rad1.grid(column=0, row=3)
rad2.grid(column=1, row=3)
rad3.grid(column=2, row=3)

#Text
lbl = Label(window, text="Don't click it")
lbl.grid(column=3, row=0)

#Click actions
def clicked():
    #lbl.configure(text="You clicked it...")
    
    #dropdown = combo.get()
    #lbl.configure(text = dropdown)
    
    #print(selected.get())
    #radio = selected.get()
    #lbl.configure(text=radio)

    #res = "" + txt.get()
    #lbl.configure(text = res)

    numbox = var.get()
    lbl.configure(text=numbox)

#Button
btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=2, row=0)

#Text box
txt = Entry(window,width=10)
txt.grid(column=1, row=0)


window.mainloop()