from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
def display():
    if(x.get()==1):
        print("Zgadzasz się!")
    else:
        print("Nie zgadzasz się :(")
class xd(tk.Tk):
    def __init__(self):
        super().__init__()
        window = self
        self.geometry("1360x650")
        tabControl = ttk.Notebook(window)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab1, text="Page 1")
        tabControl.add(tab2, text="Page 2")
        tabControl.grid()
        frame = ttk.Frame(tab1)
        photo = Image.open("D:/MelvinVSCode/AoE Draft Masta/Code/Przechwytywanie.png").resize((250, 150))
        photo = ImageTk.PhotoImage(photo)
        mylabel = tk.Label(frame, image=photo)
        mylabel.grid()
        
        frame.grid()
        
        
app = xd()
app.mainloop()
