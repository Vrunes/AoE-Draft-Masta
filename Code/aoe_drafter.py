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
        self.key = ""
        self.game_formats: dict[str, str] = {"Bo1": 1, "Bo3": 3, "Bo5": 5, 
                                        "Bo7": 7, "Bo9": 9, "Custom - not implemented": -1}
        # ToDo: add "Custom" game format
        self.formats_box = ttk.Combobox(parent, state="readonly", width=22, values=[keys for keys in self.game_formats.keys()])
        self.formats_box.bind("<<ComboboxSelected>>", self.get_selected_key)
        self.formats_box.set("Select game format")
        self.formats_box.grid(row=1, column=1, sticky="e", padx=50, pady=20)
    
    def get_selected_key(self, event=None) -> int:
        self.key = self.game_formats[self.formats_box.get()]  # changing to int, default val is string and must be for other method
        print(self.key)
        return self.key
        # messagebox.showinfo("window name", f"Format selected: {self.key}") # to remove/change


class AoEApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AoE IV Draft Master")
        self.geometry("1340x650")
        # self.resizable(False, False)
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        # page 1
        self.page_1_top_frame = ttk.Frame(self.tab1)
        self.page_1_bottom_frame = ttk.Frame(self.tab1)
        self.game_format = FormatsCombobox(self.page_1_top_frame)  # must be there to retrieve key
        self.save_indicator = tk.Label(self.page_1_top_frame, bg='red', width=3)
        self.save_indicator.grid(row=1, column=1, sticky="ne", padx=210, pady=22)
        self.page_1()
        # page 2
        self.page_2_top_frame = ttk.Frame(self.tab2)
        self.page_2_bottom_frame = ttk.Frame(self.tab2)
        self.bo_sign_page_2 = ttk.Label(self.page_2_top_frame, text="", font=("Times New Roman", 22))
        self.bo_sign_page_2.grid(row=0, column=1, sticky="e", padx=130, pady=0)

        
        self.page_2()
        # initialize pages with descriptions
        self.pages_desc()
        self.initialize_pages()
        self.maps_json: str = ""
        self.maps_json_path: str = ""
        self.existing_maps_paths: dict[str] = {}
        self.selected_maps: dict[str] = {}
        self.save_allowed: bool = False


    def page_1(self) -> None:
        button_load_map_file = ttk.Button(self.page_1_top_frame, text="Load map file", command=self.load_maps_file).grid(row=1, column=0, sticky="w", padx=50, pady=20) 
        button_set_name = ttk.Button(self.page_1_top_frame, text="Set name", command=self.set_show_name).grid(row=0, column=1, sticky="e", padx=130, pady=0)
        button_save = ttk.Button(self.page_1_top_frame, text="Save", command=self.save_page_1).grid(row=1, column=1, sticky="ne", padx=240, pady=20)        

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
        self.page_2_top_frame.columnconfigure(0, weight=1)
        self.page_2_top_frame.columnconfigure(1, weight=1)
        self.page_2_top_frame.rowconfigure(0, weight=1)
        self.page_2_top_frame.rowconfigure(1, weight=1)
        self.page_2_bottom_frame.columnconfigure(0, weight=1)
        self.page_2_bottom_frame.columnconfigure(1, weight=1)
        self.page_2_bottom_frame.rowconfigure(0, weight=1)
        self.page_2_bottom_frame.rowconfigure(1, weight=1)
        self.page_2_bottom_frame.rowconfigure(2, weight=1)
        self.page_2_bottom_frame.rowconfigure(3, weight=1)
        self.page_2_bottom_frame.rowconfigure(4, weight=1)
        self.page_2_top_frame.pack(expand=False, fill='both', side="top")
        self.page_2_bottom_frame.pack(expand=True, fill='both', side="bottom")


    def pages_desc(self) -> None:
        label_map_pool = ttk.Label(self.page_1_top_frame, text="Map pool", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_best_civs = ttk.Label(self.page_2_top_frame, text="Best civs per map", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_civs_draft = ttk.Label(self.tab3, text="Civs draft", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_game_draft = ttk.Label(self.tab4, text="Game draft", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)

    def recreate_page(self, tab: ttk.Frame, index: int = None, full_clear: bool = False) -> None:
        if index is None and full_clear:
            for item in range(len(tab.grid_slaves())):
                tab.grid_slaves()[0].destroy()  # loop for the whole frame and delete every widget (index-0 times nr of slaves)
            if tab == self.page_1_bottom_frame:
                self.selected_maps = {}
        elif index is not None and not full_clear:
            tab.grid_slaves()[index].destroy()
        print(f"cleared, widgets left: {len(tab.grid_slaves())}")

    def initialize_pages(self) -> None:
        self.tabControl.add(self.tab1, text="Page 1")
        self.tabControl.add(self.tab2, text="Page 2")
        self.tabControl.add(self.tab3, text="Page 3")
        self.tabControl.add(self.tab4, text="Page 4")
        self.tabControl.pack(expand=True, fill='both')
    

    def set_show_name(self) -> None:
        name = askstring("Input", "Enter your name (max 20 characters)")

        if len(name) > 0: 
                if len(name) > 20:
                    name = name[:20]
                label = ttk.Label(self.page_1_top_frame, text=f"Player: {name}",font=("Times New Roman", 22))
                label.grid(row=0, column=1, padx=50, pady=25, sticky="ne")
                self.recreate_page(self.page_1_top_frame, index=3)

    def load_maps_file(self) -> None:
        filename = askopenfile()

        try:
            read_file = filename.read()
            # print(json.loads(read_file))
            file_content = json.loads(read_file)
            self.maps_json = file_content  # file_content.name must be the same as folder Maps's name
            self.maps_json_path = os.getcwd() + "\\Maps\\" + file_content['name'] + "\\"
            maps_exist = self.verify_maps_exist()
        except ValueError as e:
            print("Invalid json!!")
            return None # or: raise

        if maps_exist:
            self.recreate_page(self.page_1_bottom_frame, full_clear=True)
            self.generate_maps_page_1()

    
    def verify_maps_exist(self) -> bool:
        missing_map_images: list[str] = []
        existing_maps: dict[str] = {}

        for map in self.maps_json['maps']:
            map_image_png = self.maps_json_path + map['name'] + ".png"
            map_image_jpg = self.maps_json_path + map['name'] + ".jpg"
            if not ((os.path.isfile(map_image_png)) or (os.path.isfile(map_image_jpg))):
                missing_map_images.append(map['name'])
                print(map_image_jpg, map_image_png)
            else:
                if map_image_png:
                    existing_maps[map['name']] = map_image_png
                elif map_image_jpg:
                    existing_maps[map['name']] = map_image_png
        if len(missing_map_images) == 0:
            self.existing_maps_paths = existing_maps
            return True
        else:
            print("missing map images: ", missing_map_images)
            return False

    def clicked(self, x: int, map_name: str, map_path: str) -> None:
        selected_maps = self.selected_maps  #updating selected_maps updates self.selected_maps as well
        if(x.get()==1):
            if map_name not in selected_maps:
                selected_maps[map_name] = map_path
        else:
            del selected_maps[map_name]
        self.update_save_allowed_indicator()
    
    def update_save_allowed_indicator(self) -> None:
        if len(self.selected_maps) == int(self.game_format.key):
            self.save_indicator.config(bg='green')
            self.save_allowed = True
        else:
            self.save_indicator.config(bg='red')
            self.save_allowed = False
    
    def update_bo_x_sign(self) -> None:
        self.bo_sign_page_2.config(text=f"Best of {self.game_format.key}")
        
    def save_page_1(self) -> None:
        if isinstance(self.game_format.key, int):
            self.update_save_allowed_indicator()  # reverify -> in case someone got green light and changed game format (green light stays)
        if self.save_allowed:
            self.recreate_page(self.page_2_bottom_frame, full_clear=True)
            self.update_bo_x_sign()
            self.generate_maps_page_2()
            
    def generate_maps_page_2(self) -> None:
        i = 1
        print(self.selected_maps)
        
        for name, path in self.selected_maps.items():
            print(name, path)
            photo = Image.open(path).resize((85, 85))
            if i == 1:
                best_civs_1 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_1 = sorted(set(([", ".join(civ) for civ in best_civs_1])))
                self.photo_1_page_2 = ImageTk.PhotoImage(photo)
                button_1_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_1[0]}", justify='left')
                button_1_page_2.config(font=("Arial", 12), image=self.photo_1_page_2, compound='left')
                button_1_page_2.grid(row=0, column=0, padx=50, pady=0, sticky="nw")
            elif i == 2:
                best_civs_2 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_2 = sorted(set(([", ".join(civ) for civ in best_civs_2])))
                self.photo_2_page_2 = ImageTk.PhotoImage(photo)
                button_2_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_2[0]}", justify='left')
                button_2_page_2.config(font=("Arial", 12), image=self.photo_2_page_2, compound='left')
                button_2_page_2.grid(row=1, column=0, padx=50, pady=0, sticky="nw")
            elif i == 3:
                best_civs_3 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_3 = sorted(set(([", ".join(civ) for civ in best_civs_3])))
                self.photo_3_page_2 = ImageTk.PhotoImage(photo)
                button_3_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_3[0]}", justify='left')
                button_3_page_2.config(font=("Arial", 12), image=self.photo_3_page_2, compound='left')
                button_3_page_2.grid(row=2, column=0, padx=50, pady=0, sticky="nw")
            elif i == 4:
                best_civs_4 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_4 = sorted(set(([", ".join(civ) for civ in best_civs_4])))
                self.photo_4_page_2 = ImageTk.PhotoImage(photo)
                button_4_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_4[0]}", justify='left')
                button_4_page_2.config(font=("Arial", 12), image=self.photo_4_page_2, compound='left')
                button_4_page_2.grid(row=3, column=0, padx=50, pady=0, sticky="nw")
            elif i == 5:
                best_civs_5 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_5 = sorted(set(([", ".join(civ) for civ in best_civs_5])))
                self.photo_5_page_2 = ImageTk.PhotoImage(photo)
                button_5_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_5[0]}", justify='left')
                button_5_page_2.config(font=("Arial", 12), image=self.photo_5_page_2, compound='left')
                button_5_page_2.grid(row=4, column=0, padx=50, pady=0, sticky="nw")
            elif i == 6:
                best_civs_6 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_6 = sorted(set(([", ".join(civ) for civ in best_civs_6])))
                self.photo_6_page_2 = ImageTk.PhotoImage(photo)
                button_6_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_6[0]}", justify='left')
                button_6_page_2.config(font=("Arial", 12), image=self.photo_6_page_2, compound='left')
                button_6_page_2.grid(row=0, column=1, padx=50, pady=0, sticky="nw")
            elif i == 7:
                best_civs_7 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_7 = sorted(set(([", ".join(civ) for civ in best_civs_7])))
                self.photo_7_page_2 = ImageTk.PhotoImage(photo)
                button_7_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_7[0]}", justify='left')
                button_7_page_2.config(font=("Arial", 12), image=self.photo_7_page_2, compound='left')
                button_7_page_2.grid(row=1, column=1, padx=50, pady=0, sticky="nw")
            elif i == 8:
                best_civs_8 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_8 = ", ".join(sorted(set(([", ".join(civ) for civ in best_civs_8]))))
                self.photo_8_page_2 = ImageTk.PhotoImage(photo)
                button_8_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_8[0]}", justify='left')
                button_8_page_2.config(font=("Arial", 12), image=self.photo_8_page_2, compound='left')
                button_8_page_2.grid(row=2, column=1, padx=50, pady=0, sticky="nw")
            elif i == 9:
                best_civs_9 = [i["best_civs"] for i in self.maps_json['maps'] if i.get("name") == name]
                best_civs_9 = sorted(set(([", ".join(civ) for civ in best_civs_9])))
                self.photo_9_page_2 = ImageTk.PhotoImage(photo)
                button_9_page_2 = tk.Label(self.page_2_bottom_frame, text=f" {name}\n\n\n Best civs for map: {best_civs_9[0]}", justify='left')
                button_9_page_2.config(font=("Arial", 12), image=self.photo_9_page_2, compound='left')
                button_9_page_2.grid(row=3, column=1, padx=50, pady=0, sticky="nw")
            i+=1

    def generate_maps_page_1(self):

        if len(self.maps_json['maps']) > 16:
            print(f"Map count exceeds supported 16 maps generation. Maps in file: {len(self.maps_json['maps'])}")
            return
        else:
            i = 1
            for map in self.maps_json['maps']:
                map_name = map['name']
                map_path = self.existing_maps_paths[map_name]
                # print("name: ", map_name, "path: ", map_path)
                photo = Image.open(map_path).resize((55, 55))
                if i == 1:
                    x_1 = tk.IntVar()
                    map_name_1 = map_name
                    map_path_1 = map_path
                    self.photo_1 = ImageTk.PhotoImage(photo)
                    button_1 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_1}", variable=x_1, onvalue=1, offvalue=0, command=lambda:self.clicked(x_1, map_name_1, map_path_1))
                    button_1.config(font=("Arial", 12), image=self.photo_1, compound='left')
                    button_1.grid(row=0, column=0, padx=50, pady=0, sticky="nw")
                elif i == 2:
                    x_2 = tk.IntVar()
                    map_name_2 = map_name
                    map_path_2 = map_path
                    self.photo_2 = ImageTk.PhotoImage(photo)
                    button_2 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_2}", variable=x_2, onvalue=1, offvalue=0, command=lambda:self.clicked(x_2, map_name_2, map_path_2))
                    button_2.config(font=("Arial", 12), image=self.photo_2, compound='left')
                    button_2.grid(row=1, column=0, padx=50, pady=0, sticky="nw")
                elif i == 3:
                    x_3 = tk.IntVar()
                    map_name_3 = map_name
                    map_path_3 = map_path
                    self.photo_3 = ImageTk.PhotoImage(photo)
                    button_3 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_3}", variable=x_3, onvalue=1, offvalue=0, command=lambda:self.clicked(x_3, map_name_3, map_path_3))
                    button_3.config(font=("Arial", 12), image=self.photo_3, compound='left')
                    button_3.grid(row=2, column=0, padx=50, pady=0, sticky="nw")
                elif i == 4:
                    x_4 = tk.IntVar()
                    map_name_4 = map_name
                    map_path_4 = map_path
                    self.photo_4 = ImageTk.PhotoImage(photo)
                    button_4 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_4}", variable=x_4, onvalue=1, offvalue=0, command=lambda:self.clicked(x_4, map_name_4, map_path_4))
                    button_4.config(font=("Arial", 12), image=self.photo_4, compound='left')
                    button_4.grid(row=3, column=0, padx=50, pady=0, sticky="nw")
                elif i == 5:
                    x_5 = tk.IntVar()
                    map_name_5 = map_name
                    map_path_5 = map_path
                    self.photo_5 = ImageTk.PhotoImage(photo)
                    button_5 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_5}", variable=x_5, onvalue=1, offvalue=0, command=lambda:self.clicked(x_5, map_name_5, map_path_5))
                    button_5.config(font=("Arial", 12), image=self.photo_5, compound='left')
                    button_5.grid(row=0, column=1, padx=50, pady=0, sticky="nw")
                elif i == 6:
                    x_6 = tk.IntVar()
                    map_name_6 = map_name
                    map_path_6 = map_path
                    self.photo_6 = ImageTk.PhotoImage(photo)
                    button_6 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_6}", variable=x_6, onvalue=1, offvalue=0, command=lambda:self.clicked(x_6, map_name_6, map_path_6))
                    button_6.config(font=("Arial", 12), image=self.photo_6, compound='left')
                    button_6.grid(row=1, column=1, padx=50, pady=0, sticky="nw")
                elif i == 7:
                    x_7 = tk.IntVar()
                    map_name_7 = map_name
                    map_path_7 = map_path
                    self.photo_7 = ImageTk.PhotoImage(photo)
                    button_7 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_7}", variable=x_7, onvalue=1, offvalue=0, command=lambda:self.clicked(x_7, map_name_7, map_path_7))
                    button_7.config(font=("Arial", 12), image=self.photo_7, compound='left')
                    button_7.grid(row=2, column=1, padx=50, pady=0, sticky="nw")
                elif i == 8:
                    x_8 = tk.IntVar()
                    map_name_8 = map_name
                    map_path_8 = map_path
                    self.photo_8 = ImageTk.PhotoImage(photo)
                    button_8 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_8}", variable=x_8, onvalue=1, offvalue=0, command=lambda:self.clicked(x_8, map_name_8, map_path_8))
                    button_8.config(font=("Arial", 12), image=self.photo_8, compound='left')
                    button_8.grid(row=3, column=1, padx=50, pady=0, sticky="nw")
                elif i == 9:
                    x_9 = tk.IntVar()
                    map_name_9 = map_name
                    map_path_9 = map_path
                    self.photo_9 = ImageTk.PhotoImage(photo)
                    button_9 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_9}", variable=x_9, onvalue=1, offvalue=0, command=lambda:self.clicked(x_9, map_name_9, map_path_9))
                    button_9.config(font=("Arial", 12), image=self.photo_9, compound='left')
                    button_9.grid(row=4, column=0, padx=50, pady=0, sticky="nw")
                elif i == 10:
                    x_10 = tk.IntVar()
                    map_name_10 = map_name
                    map_path_10 = map_path
                    self.photo_10 = ImageTk.PhotoImage(photo)
                    button_10 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_10}", variable=x_10, onvalue=1, offvalue=0, command=lambda:self.clicked(x_10, map_name_10, map_path_10))
                    button_10.config(font=("Arial", 12), image=self.photo_10, compound='left')
                    button_10.grid(row=5, column=0, padx=50, pady=0, sticky="nw")
                elif i == 11:
                    x_11 = tk.IntVar()
                    map_name_11 = map_name
                    map_path_11 = map_path
                    self.photo_11 = ImageTk.PhotoImage(photo)
                    button_11 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_11}", variable=x_11, onvalue=1, offvalue=0, command=lambda:self.clicked(x_11, map_name_11, map_path_11))
                    button_11.config(font=("Arial", 12), image=self.photo_11, compound='left')
                    button_11.grid(row=6, column=0, padx=50, pady=0, sticky="nw")
                elif i == 12:
                    x_12 = tk.IntVar()
                    map_name_12 = map_name
                    map_path_12 = map_path
                    self.photo_12 = ImageTk.PhotoImage(photo)
                    button_12 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_12}", variable=x_12, onvalue=1, offvalue=0, command=lambda:self.clicked(x_12, map_name_12, map_path_12))
                    button_12.config(font=("Arial", 12), image=self.photo_12, compound='left')
                    button_12.grid(row=7, column=0, padx=50, pady=0, sticky="nw")
                elif i == 13:
                    x_13 = tk.IntVar()
                    map_name_13 = map_name
                    map_path_13 = map_path
                    self.photo_13 = ImageTk.PhotoImage(photo)
                    button_13 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_13}", variable=x_13, onvalue=1, offvalue=0, command=lambda:self.clicked(x_13, map_name_13, map_path_13))
                    button_13.config(font=("Arial", 12), image=self.photo_13, compound='left')
                    button_13.grid(row=4, column=1, padx=50, pady=0, sticky="nw")
                elif i == 14:
                    x_14 = tk.IntVar()
                    map_name_14 = map_name
                    map_path_14 = map_path
                    self.photo_14 = ImageTk.PhotoImage(photo)
                    button_14 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_14}", variable=x_14, onvalue=1, offvalue=0, command=lambda:self.clicked(x_14, map_name_14, map_path_14))
                    button_14.config(font=("Arial", 12), image=self.photo_14, compound='left')
                    button_14.grid(row=5, column=1, padx=50, pady=0, sticky="nw")
                elif i == 15:
                    x_15 = tk.IntVar()
                    map_name_15 = map_name
                    map_path_15 = map_path
                    self.photo_15 = ImageTk.PhotoImage(photo)
                    button_15 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_15}", variable=x_15, onvalue=1, offvalue=0, command=lambda:self.clicked(x_15, map_name_15, map_path_15))
                    button_15.config(font=("Arial", 12), image=self.photo_15, compound='left')
                    button_15.grid(row=6, column=1, padx=50, pady=0, sticky="nw")
                elif i == 16:
                    x_16 = tk.IntVar()
                    map_name_16 = map_name
                    map_path_16 = map_path
                    self.photo_16 = ImageTk.PhotoImage(photo)
                    button_16 = tk.Checkbutton(self.page_1_bottom_frame, text=f" {map_name_16}", variable=x_16, onvalue=1, offvalue=0, command=lambda:self.clicked(x_16, map_name_16, map_path_16))
                    button_16.config(font=("Arial", 12), image=self.photo_16, compound='left')
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
