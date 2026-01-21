import json
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
        self.formats_box.pack(side=tk.TOP, anchor="e", padx=140, pady=20)
    
    def get_selected_key(self, event=None) -> str:
        self.key = self.formats_box.get()
        print(self.key)
        # messagebox.showinfo("window name", f"Format selected: {self.key}") # to remove/change
        return self.key


class AoEApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TEST")
        self.geometry("1240x650")
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.initialize_pages()
        self.pages_desc()
        self.page_1()
        self.page_32 = self.page_2()
        self.maps_json: str = ""
        self.game_format: str = ""

        # print(self.page_32)
        # frame.grid(row=0, column=0, padx=1000, pady=15)



    def page_1(self) -> None:
        button = ttk.Button(self.tab1, text="Set name", command=self.set_show_name).pack(side=tk.TOP, anchor="e", padx=140, pady=25)
        button2 = ttk.Button(self.tab1, text="Load map file", command=self.load_maps_file).place(x=100, y=65)
        game_format = FormatsCombobox(self.tab1)
        
    
    def page_2(self) -> None:
        pass
        # return label_map_pool2
    
    def pages_desc(self) -> None:
        label_map_pool = ttk.Label(self.tab1, text="Map pool", font=("Times New Roman", 22)).pack(side=tk.TOP, anchor="w", padx=50, pady=25)
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
    



    def recreate_page(self) -> None:
        """ needs testing """
        print(len(self.tab2.pack_slaves()), self.tab2.pack_slaves())
        xd = [self.tab2.pack_slaves()[0].destroy()]

    def initialize_pages(self) -> None:
        self.tabControl.add(self.tab1, text="Page 1")
        self.tabControl.add(self.tab2, text="Page 2")
        self.tabControl.add(self.tab3, text="Page 3")
        self.tabControl.add(self.tab4, text="Page 4")
        self.tabControl.pack(expand=1, fill="both")

    def set_show_name(self) -> None:
        name = askstring("Input", "Enter your name")

        if len(name) > 0: 
                label = ttk.Label(self, text="", font=("Arial", 22))
                label.config(text=f"Player: {name}")
                label.place(x=1000, y=45)

    def load_maps_file(self) -> None:
        filename = askopenfile()
        
        try:
            read_file = filename.read()
            print(json.loads(read_file))
            self.maps_json = json.loads(read_file)
        except ValueError as e:
            print("Invalid json!!")
            return None # or: raise

        # print(name)
    # def main_window(self):
    #     xd = tk.Label(text="Test2", width=170, height=45)
    #     xd.pack()




# class InputForm(ttk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent)

#         self.columnconfigure(0, weight=1)
#         self.rowconfigure(1, weight=1)

#         self.entry = ttk.Entry(self)
#         self.entry.grid(row=0, column=0, sticky="ew")
#         self.entry.bind("<Return>", self.add_to_list)

#         self.entry_btn = ttk.Button(self, text="Add", command=self.add_to_list)
#         self.entry_btn.grid(row=0, column=1)

#         self.text_list = tk.Listbox(self)
#         self.text_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
    
#     def add_to_list(self, event=None):
#         text = self.entry.get()
#         if text:
#             self.text_list.insert(tk.END, text)
#             self.entry.delete(0, tk.END)



if __name__ == "__main__":
    main()
