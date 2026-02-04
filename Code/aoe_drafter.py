import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        self.formats_box.grid(row=0, column=1, sticky="ne", padx=50, pady=85)
    
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
        self.resizable(False, False)
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)

        # page 1
        self.page_1_top_frame = ttk.Frame(self.tab1, height=100)
        self.page_1_bottom_frame = ttk.Frame(self.tab1, height=550)
        self.page_1()
        
        self.pages_desc()
        self.page_2()
        self.initialize_pages()

        self.maps_json: str = ""
        self.maps_json_path: str = ""
        self.existing_maps: list[str] = []
        self.game_format: str = ""

        # print(self.page_32)
        # frame.grid(row=0, column=0, padx=1000, pady=15)



    def page_1(self) -> None:
        button_load_map_file = ttk.Button(self.page_1_top_frame, text="Load map file", command=self.load_maps_file).grid(row=0, column=0, sticky="nw", padx=50, pady=100)
        game_format = FormatsCombobox(self.page_1_top_frame)
        button_set_name = ttk.Button(self.page_1_top_frame, text="Set name", command=self.set_show_name).grid(row=0, column=1, sticky="ne", padx=130, pady=25)
        button_save = ttk.Button(self.page_1_top_frame, text="Save", command=self.set_show_name, ).grid(row=0, column=1, sticky="ne", padx=240, pady=85)
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
        pass
        # return label_map_pool2
    
    def pages_desc(self) -> None:
        label_map_pool = ttk.Label(self.page_1_top_frame, text="Map pool", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_best_civs = ttk.Label(self.tab2, text="Best civs per map", font=("Times New Roman", 22)).pack(side=tk.TOP, anchor="w", padx=50, pady=25)
        label_civs_draft = ttk.Label(self.tab3, text="Civs draft", font=("Times New Roman", 22)).pack(side=tk.TOP, anchor="w", padx=50, pady=25)
        label_game_draft = ttk.Label(self.tab4, text="Game draft", font=("Times New Roman", 22)).pack(side=tk.TOP, anchor="w", padx=50, pady=25)





    def recreate_page(self, tab: ttk.Frame) -> None:
        """ needs testing """
        # for item in tab.grid_slaves():
        #     print(item)
        tab.grid_slaves()[5].destroy()

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
    
    def generate_maps_page_1(self):
        i = 0
        print(self.existing_maps)
        if len(self.maps_json['maps']) > 16:
            print(f"Map count exceeds supported 16 maps generation. Maps in file: {len(self.maps_json['maps'])}")
            return
        else:
            for map in self.maps_json['maps']:
                if i == 0:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=0, column=0, padx=50, pady=0, sticky="nw")
                elif i == 1:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=1, column=0, padx=50, pady=0, sticky="nw")
                elif i == 2:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=2, column=0, padx=50, pady=0, sticky="nw")
                elif i == 3:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=3, column=0, padx=50, pady=0, sticky="nw")
                elif i == 4:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=0, column=1, padx=50, pady=0, sticky="nw")
                elif i == 5:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=1, column=1, padx=50, pady=0, sticky="nw")
                elif i == 6:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=2, column=1, padx=50, pady=0, sticky="nw")
                elif i == 7:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=3, column=1, padx=50, pady=0, sticky="nw")
                elif i == 8:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=4, column=0, padx=50, pady=0, sticky="nw")
                elif i == 9:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=5, column=0, padx=50, pady=0, sticky="nw")
                elif i == 10:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=6, column=0, padx=50, pady=0, sticky="nw")
                elif i == 11:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=7, column=0, padx=50, pady=0, sticky="nw")
                elif i == 12:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=4, column=1, padx=50, pady=0, sticky="nw")
                elif i == 13:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=5, column=1, padx=50, pady=0, sticky="nw")
                elif i == 14:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=6, column=1, padx=50, pady=0, sticky="nw")
                elif i == 15:
                    button = ttk.Checkbutton(self.page_1_bottom_frame, text=f"{map['name']}")
                    button.grid(row=7, column=1, padx=50, pady=0, sticky="nw")
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
