### pip3 install pyperclip Tk
import tkinter as tk
import pyperclip
from functools import partial
import webbrowser
top = tk.Tk()

texts = {
    # Title                       : Content
    "-- BEUREKA2"                 : "https://shopee.sg/beureka",
    "-- Shopee"                   : "https://shopee.sg/",
    "-- Eunoiia"                  : "https://shopee.sg/uid={0}",
}


def copyTxt(txt, entry=None):
    if entry:
        print(txt, entry.get())
        webbrowser.open(txt.format(entry.get().strip()))
    else:
        webbrowser.open(txt)
    # ret = pyperclip.copy(txt)
    # ret = pyperclip.paste()
    # print(f'copied {txt} to clipboard - ret:{ret}')

for k in texts.keys():
    if '{0}' in texts[k]:
        label = tk.Label(textvariable='------')
        label.pack()
        entry = tk.Entry()
        entry.pack()
        g = partial(copyTxt, texts[k], entry)
        B = tk.Button(top, text=k, command=g)
        B.pack()
    else:
        g = partial(copyTxt, texts[k])
        B = tk.Button(top, text=k, command=g)
        B.pack()

top.title("James' LinkBot")
top.resizable(False, False)
top.attributes('-toolwindow',True)
top.attributes('-topmost',True)
top.mainloop()
