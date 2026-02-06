import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.simpledialog import askstring
from tkinter.filedialog import askopenfile


def main() -> None:
    app = AoEApplication()
    app.mainloop()


class FormatsCombobox(ttk.Combobox):
    def __init__(self, parent):
        self.parent = parent
        self.key: str = ""
        game_formats: list[str] = ["Bo1", "Bo3", "Bo5", "Bo7", "Bo9", "Custom - not implemented"]
        # ToDo: add "Custom" game format
        self.formats_box = ttk.Combobox(parent, state="readonly", width=22, values=game_formats)
        self.formats_box.bind("<<ComboboxSelected>>", self.get_selected_key)
        self.formats_box.set("Select game format")
        self.formats_box.grid(row=1, column=1, sticky="e", padx=50, pady=0)
    
    def get_selected_key(self, event=None) -> str:
        self.key = self.formats_box.get()
        print(self.key)
        # messagebox.showinfo("window name", f"Format selected: {self.key}") # to remove/change
        return self.key


class AoEApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TEST")
        self.geometry("1340x650")
        # self.resizable(False, False)
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        # self.photo = Image.open("D:/MelvinVSCode/AoE Draft Masta/Code/Przechwytywanie.png").resize((250, 250))
        # self.photo = ImageTk.PhotoImage(self.photo)
        # page 1
        self.page_1_top_frame = ttk.Frame(self.tab1)
        self.page_1_bottom_frame = ttk.Frame(self.tab1)
        self.page_1()
        # page 2
        self.page_2_frame = ttk.Frame(self.tab2)
        
        self.page_2()
        # initialize pages with descriptions
        self.pages_desc()
        self.initialize_pages()
        self.maps_json: str = ""
        self.maps_json_path: str = ""
        self.existing_maps: list[str] = []
        self.game_format: str = ""
        self.mainloop()
        # print(self.page_32)
        # frame.grid(row=0, column=0, padx=1000, pady=15)


    def page_1(self) -> None:
        button_load_map_file = ttk.Button(self.page_1_top_frame, text="Load map file", command=self.load_maps_file).grid(row=1, column=0, sticky="w", padx=50, pady=0)
        game_format = FormatsCombobox(self.page_1_top_frame)
        button_set_name = ttk.Button(self.page_1_top_frame, text="Set name", command=self.set_show_name).grid(row=0, column=1, sticky="e", padx=130, pady=0)
        button_save = ttk.Button(self.page_1_top_frame, text="Save", command=self.set_show_name, ).grid(row=1, column=1, sticky="ne", padx=240, pady=0)
        # button_save = ttk.Button(self.page_1_bottom_frame, text="Save", command=self.set_show_name, ).grid(row=0, column=1, sticky="ns", padx=240, pady=0)
        # button_save = ttk.Button(self.page_1_bottom_frame, text="Save", command=self.set_show_name, ).grid(row=1, column=1, sticky="ns", padx=240, pady=0)

        self.page_1_top_frame.columnconfigure(0, weight=1)
        self.page_1_top_frame.columnconfigure(1, weight=1)
        self.page_1_top_frame.rowconfigure(0, weight=1)
        self.page_1_top_frame.rowconfigure(1, weight=1)
        self.page_1_bottom_frame.columnconfigure(0, weight=1)
        self.page_1_bottom_frame.columnconfigure(1, weight=1)
        self.page_1_bottom_frame.rowconfigure(0, weight=1)
        self.page_1_bottom_frame.rowconfigure(1, weight=1)
        self.page_1_bottom_frame.rowconfigure(2, weight=1)
        self.page_1_bottom_frame.rowconfigure(3, weight=1)
        self.page_1_bottom_frame.rowconfigure(4, weight=1)
        self.page_1_bottom_frame.rowconfigure(5, weight=1)
        self.page_1_bottom_frame.rowconfigure(6, weight=1)
        self.page_1_bottom_frame.rowconfigure(7, weight=1)
        self.page_1_top_frame.pack(expand=False, fill='both', side="top")
        self.page_1_bottom_frame.pack(expand=True, fill='both', side="bottom")
        
    
    def page_2(self) -> None:
        # photo = Image.open("D:/MelvinVSCode/AoE Draft Masta/Code/Przechwytywanie.png").resize((250, 250))
        # self.photo = ImageTk.PhotoImage(photo)
        # mylabel = tk.Label(self.page_2_frame, image=self.photo, background='black')
        # mylabel.grid(row=1, column=1)
        # checkbutton = tk.Checkbutton(self.page_2_main_frame, text="hahaha", image=photo)
        # checkbutton.grid(row=0, column=0, sticky="")
        self.page_2_frame.columnconfigure(0, weight=1)
        self.page_2_frame.columnconfigure(1, weight=1)
        self.page_2_frame.rowconfigure(0, weight=1)
        self.page_2_frame.rowconfigure(1, weight=1)
        self.page_2_frame.pack(expand=True, fill='both', side="bottom")
    
    def pages_desc(self) -> None:
        label_map_pool = ttk.Label(self.page_1_top_frame, text="Map pool", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_best_civs = ttk.Label(self.page_2_frame, text="Best civs per map", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_civs_draft = ttk.Label(self.tab3, text="Civs draft", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_game_draft = ttk.Label(self.tab4, text="Game draft", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)





    def recreate_page(self, tab: ttk.Frame) -> None:
        """ needs testing """
        # for item in tab.grid_slaves():
        #     print(item)
        print(tab.grid_slaves())
        tab.grid_slaves()[3].destroy()

    def initialize_pages(self) -> None:
        # self.tab1.pack(expand=True, fill='both')
        # self.tab1.columnconfigure(0, weight=1)
        # self.tab1.columnconfigure(1, weight=1)
        # self.tab1.rowconfigure(0, weight=1)
        # self.tab1.rowconfigure(1, weight=4)
        self.tabControl.add(self.tab1, text="Page 1")
        self.tabControl.add(self.tab2, text="Page 2")
        self.tabControl.add(self.tab3, text="Page 3")
        self.tabControl.add(self.tab4, text="Page 4")
        self.tabControl.pack(expand=True, fill='both')
    
        # self.tabControl.grid(row=0, column=0)

    def set_show_name(self) -> None:
        name = askstring("Input", "Enter your name")

        if len(name) > 0: 
                label = ttk.Label(self.page_1_top_frame, text=f"Player: {name}",font=("Times New Roman", 22))
                label.grid(row=0, column=1, padx=50, pady=25, sticky="ne")
                self.recreate_page(self.page_1_top_frame)

    def load_maps_file(self) -> None:
        filename = askopenfile()
        
        try:
            read_file = filename.read()
            # print(json.loads(read_file))
            file_content = json.loads(read_file)
            self.maps_json = file_content
            self.maps_json_path = self.maps_json_path.join(os.getcwd() + "\\Maps\\" + file_content['name'] + "\\")
            maps_exist = self.verify_maps_exist()
        except ValueError as e:
            print("Invalid json!!")
            return None # or: raise
        
        if maps_exist:
            self.generate_maps_page_1()

    
    def verify_maps_exist(self) -> bool:
        missing_map_images: list[str] = []
        existing_maps: list[str] = []

        for map in self.maps_json['maps']:
            map_image_png = self.maps_json_path + map['name'] + ".png"
            map_image_jpg = self.maps_json_path + map['name'] + ".jpg"
            if not ((os.path.isfile(map_image_png)) or (os.path.isfile(map_image_jpg))):
                missing_map_images.append(map['name'])
            else:
                if map_image_png:
                    existing_maps.append(map_image_png)
                elif map_image_jpg:
                    existing_maps.append(map_image_jpg)
        self.existing_maps = existing_maps

        if len(missing_map_images) == 0:
            return True
        else:
            print("missing map images: ", missing_map_images)
            return False
    
    def display(self, x):
        if(x.get()==1):
            print("On")
        else:
            print("Off")
            
    def generate_maps_page_1(self):
        i = 1
        x = tk.IntVar()
        print(os.getcwd())
        photo = Image.open(os.getcwd()+"\\Maps\\"+"Road to Wololo Londinium\\Socotra.png").resize((45, 45))
        self.photo = ImageTk.PhotoImage(photo)
        # print(self.existing_maps)
        if len(self.maps_json['maps']) > 16:
            print(f"Map count exceeds supported 16 maps generation. Maps in file: {len(self.maps_json['maps'])}")
            return
        else:
            for map in self.maps_json['maps']:
                # print(self.existing_maps[i])
                
                if i == 1:
                    button_1 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}", variable=x, onvalue=1, offvalue=0, command=lambda:self.display(x))
                    button_1.config(font=("Arial", 12), image=self.photo, compound='right')
                    button_1.grid(row=0, column=0, padx=50, pady=0, sticky="nw")
                elif i == 2:
                    button_2 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_2.config(font=("Arial", 12), image=self.photo, compound='right')
                    button_2.grid(row=1, column=0, padx=50, pady=0, sticky="nw")
                elif i == 3:
                    button_3 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_3.config(font=("Arial", 12), image=self.photo, compound='right')
                    button_3.grid(row=2, column=0, padx=50, pady=0, sticky="nw")
                elif i == 4:
                    button_4 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_4.config(font=("Arial", 12), image=self.photo, compound='right')
                    button_4.grid(row=3, column=0, padx=50, pady=0, sticky="nw")
                elif i == 5:
                    button_5 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_5.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_5.grid(row=0, column=1, padx=50, pady=0, sticky="nw")
                elif i == 6:
                    button_6 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_6.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_6.grid(row=1, column=1, padx=50, pady=0, sticky="nw")
                elif i == 7:
                    button_7 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_7.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_7.grid(row=2, column=1, padx=50, pady=0, sticky="nw")
                elif i == 8:
                    button_8 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_8.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_8.grid(row=3, column=1, padx=50, pady=0, sticky="nw")
                elif i == 9:
                    button_9 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_9.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_9.grid(row=4, column=0, padx=50, pady=0, sticky="nw")
                elif i == 10:
                    button_10 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_10.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_10.grid(row=5, column=0, padx=50, pady=0, sticky="nw")
                elif i == 11:
                    button_11 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_11.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_11.grid(row=6, column=0, padx=50, pady=0, sticky="nw")
                elif i == 12:
                    button_12 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_12.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_12.grid(row=7, column=0, padx=50, pady=0, sticky="nw")
                elif i == 13:
                    button_13 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_13.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_13.grid(row=4, column=1, padx=50, pady=0, sticky="nw")
                elif i == 14:
                    button_14 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_14.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_14.grid(row=5, column=1, padx=50, pady=0, sticky="nw")
                elif i == 15:
                    button_15 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_15.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_15.grid(row=6, column=1, padx=50, pady=0, sticky="nw")
                elif i == 16:
                    button_16 = tk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button_16.config(font=("Arial", 12), image=self.photo, compound='left')
                    button_16.grid(row=7, column=1, padx=50, pady=0, sticky="nw")
                i+=1
        # for map in self.maps_json['maps']:
        #     print(map['name'])
        #     button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
        #     button.grid(row=1, column=0, padx=40*i, pady=0, sticky="nw")
        #     i+= 1


        # print(name)
    # def main_window(self):
    #     xd = tk.Label(text="Test2", width=170, height=45)
    #     xd.pack()




if __name__ == "__main__":
    main()
