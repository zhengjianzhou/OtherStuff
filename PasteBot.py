### pip3 install pyperclip Tk
import tkinter as tk
import pyperclip
from functools import partial
top = tk.Tk()

texts = {
    # Title     : Content
    "button1" : "Please don't let this guy to do the work",
    "button2" : "Please don't let this guy to do the work",
    "button3" : "Please don't let this guy to do the work",
    "button4" : "Please don't let this guy to do the work",
}


def copyTxt(txt):
    ret = pyperclip.copy(txt)
    # ret = pyperclip.paste()
    print(f'copied {txt} to clipboard - ret:{ret}')

for k in texts.keys():
    g = partial(copyTxt, texts[k])
    B = tk.Button(top, text=k, command=g)
    B.pack()

top.title("James' PasteBot")
top.resizable(False, False)
top.attributes('-toolwindow',True)
top.attributes('-topmost',True)
top.mainloop()
