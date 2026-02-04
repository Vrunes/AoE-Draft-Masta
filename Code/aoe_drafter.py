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
        # self.formats_box.pack(side=tk.TOP, anchor="e", padx=140, pady=20)
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
        # self.resizable(False, False)
        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand=True, fill='both')
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)

        
        self.page_1()
        self.pages_desc()
        self.page_2()
        self.initialize_pages()

        self.maps_json: str = ""
        self.maps_json_path: str = ""
        self.game_format: str = ""

        # print(self.page_32)
        # frame.grid(row=0, column=0, padx=1000, pady=15)



    def page_1(self) -> None:
        # self.top_frame = tk.Frame(self.tab1, width=0, height=0, bg='lightblue')
        # self.top_frame.grid(row=0, column=0, padx=0, pady=0)
        # self.tabControl.add(self.bottom_frame, text="Page 3")
        button_set_name = ttk.Button(self.tab1, text="Set name", command=self.set_show_name).grid(row=0, column=1, sticky="ne", padx=130, pady=25)
        button_save = ttk.Button(self.tab1, text="Save", command=self.set_show_name).grid(row=0, column=1, sticky="ne", padx=240, pady=85)
        button2 = ttk.Button(self.tab1, text="Load map file", command=self.load_maps_file).grid(row=0, column=0, sticky="nw", padx=50, pady=100)
        game_format = FormatsCombobox(self.tab1)
        # self.bottom_frame = tk.Frame(self.tab1, width=10, height=10, bg='green')
        # self.bottom_frame.grid(row=1, column=0, padx=0, pady=0)
        # button_bottom_frame = ttk.Button(self.bottom_frame, text="Set name bottom frame", command=None).grid(row=0, column=0, sticky="w", padx=1040, pady=220)

        
    
    def page_2(self) -> None:
        pass
        # return label_map_pool2
    
    def pages_desc(self) -> None:
        label_map_pool = ttk.Label(self.tab1, text="Map pool", font=("Times New Roman", 22)).grid(row=0, column=0, sticky='nw', padx=50, pady=25)
        label_best_civs = ttk.Label(self.tab2, text="Best civs per map", font=("Times New Roman", 22)).pack(side=tk.TOP, anchor="w", padx=50, pady=25)
        label_civs_draft = ttk.Label(self.tab3, text="Civs draft", font=("Times New Roman", 22)).pack(side=tk.TOP, anchor="w", padx=50, pady=25)
        label_game_draft = ttk.Label(self.tab4, text="Game draft", font=("Times New Roman", 22)).pack(side=tk.TOP, anchor="w", padx=50, pady=25)



        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)
        # self.rowconfigure(0, weight=1)

        # frame = InputForm(self)
        # frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # frame2 = InputForm(self)
        # frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    



    def recreate_page(self, tab: ttk.Frame) -> None:
        """ needs testing """
        # for item in tab.grid_slaves():
        #     print(item)
        tab.grid_slaves()[5].destroy()

    def initialize_pages(self) -> None:
        self.tab1.pack(expand=True, fill='both')
        self.tab1.columnconfigure(0, weight=1)
        self.tab1.columnconfigure(1, weight=1)
        self.tab1.rowconfigure(0, weight=1)
        self.tab1.rowconfigure(1, weight=1)
        # self.tab1.columnconfigure(2, weight=1)
        # self.tab1.columnconfigure(3, weight=1)
        # self.tab1.rowconfigure(2, weight=1)
        # self.tab1.rowconfigure(3, weight=1)
        self.tabControl.add(self.tab1, text="Page 1")
        self.tabControl.add(self.tab2, text="Page 2")
        self.tabControl.add(self.tab3, text="Page 3")
        self.tabControl.add(self.tab4, text="Page 4")
        # self.tabControl.grid(row=0, column=0)

    def set_show_name(self) -> None:
        name = askstring("Input", "Enter your name")

        if len(name) > 0: 
                label = ttk.Label(self.tab1, text=f"Player: {name}",font=("Times New Roman", 22))
                label.grid(row=0, column=1, padx=50, pady=25, sticky="ne")
                self.recreate_page(self.tab1)

    def load_maps_file(self) -> None:
        filename = askopenfile()
        
        try:
            read_file = filename.read()
            print(json.loads(read_file))
            file_content = json.loads(read_file)
            # print(read_file)
            self.maps_json = file_content
            # self.maps_json = read_file
            # print(self.maps_json['maps'])
            self.maps_json_path = self.maps_json_path.join(os.getcwd() + "\\Maps\\" + file_content['name'] + "\\")
            self.verify_maps_exist()
        except ValueError as e:
            print("Invalid json!!")
            return None # or: raise
    
    def verify_maps_exist(self) -> None:
        missing_map_images: list[str] = []

        for map in self.maps_json['maps']:
            map_image_png = self.maps_json_path + map['name'] + ".png"
            map_image_jpg = self.maps_json_path + map['name'] + ".jpg"
            if not ((os.path.isfile(map_image_png)) or (os.path.isfile(map_image_jpg))):
                missing_map_images.append(map['name'])
        if len(missing_map_images) > 0:
            print("missing map images: ", missing_map_images)



        # print(name)
    # def main_window(self):
    #     xd = tk.Label(text="Test2", width=170, height=45)
    #     xd.pack()




if __name__ == "__main__":
    main()
