from pprint import pp
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
import os

def setup_menu():
    global root

    menubar = tk.Menu(root)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=new_file)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Save as", command=save_file_as)
    filemenu.add_command(label="Close", command=close_file)
    menubar.add_cascade(label="File", menu=filemenu)

    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Find", command=open_search_area)
    global replace_area
    edit_menu.add_command(label="Replace", command=lambda: replace_area.grid())
    menubar.add_cascade(label="Edit", menu=edit_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    global about_area
    help_menu.add_command(label="About", command=lambda: AboutWindow(root))
    menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)

def open_search_area():
    search_area.grid()

def check_if_changes_not_saved():
    if edit_area.text.get("1.0", "end").strip() == "":
        return

    print( edit_area.text.get("1.0", "end"))

    file_name = os.path.basename(current_file_path)
    answer = tk.messagebox.askyesno(title="Unsaved Changes", message=f"File {file_name} has unsaved changes. Do you wish to save them?")
    if answer == True:
        save_file()

def close_file():
    global edit_area
    global root
    global current_file_path

    check_if_changes_not_saved()

    edit_area.text.delete('1.0', "end")
    root.title("Notepad")
    current_file_path = ""

    info_bar.update()

def save_file():
    if current_file_path == "":
        save_file_as()
        return

    file = open(current_file_path, "w")
    contents = edit_area.text.get("1.0", "end")
    file.write(contents)
    file.close()

def save_file_as(file_path=None):
    global current_file_path

    if file_path == None:
        file_path = filedialog.asksaveasfilename()
        if file_path == () or file_path == "":
            return
        current_file_path = file_path

    file = open(current_file_path, "w")
    contents = edit_area.text.get("1.0", "end")
    file.write(contents)
    file.close()

def new_file(file_name=None):
    close_file()

def open_file(file_path=None):
    global edit_area
    global root
    global current_file_path

    if file_path == None:
        file_path = filedialog.askopenfilename()
        if file_path == () or file_path == "":
            return
        current_file_path = file_path

    file_name = os.path.basename(file_path)
    root.title(f"Notepad - {file_name}")

    close_file()
    file = open(file_path, "r")
    contents = file.read()
    edit_area.text.insert(1.0, contents)
    file.close()

class AboutWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title("About")
        self.geometry("350x350")
        self.title_label = tk.Label(self, text="Notepad", font=("Times New Roman", 20))
        self.title_label.pack()
        self.description_label = tk.Label(self, text="A small notepad like application made\n in python tkinter by JeffTheK")
        self.description_label.pack()

class EditArea(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.text = scrolledtext.ScrolledText(self)
        self.text.pack(fill="both", expand=True)
        font = tkfont.Font(font=self.text['font'])
        self.tab_string = "    "
        tab_size = font.measure(self.tab_string)
        self.text.config(tabs=tab_size)

class InfoBar(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.position_label = ttk.Label(self, text="Ln 1, Col 0")
        self.position_label.grid(row=0, column=1, sticky="e")

        self.tab_size_label = ttk.Label(self, text=f"Tab Size: {len(edit_area.tab_string)}")
        self.tab_size_label.grid(row=0, column=0, sticky="e", padx=10)

    def update(self):
        position = edit_area.text.index(tk.INSERT)
        position = position.split(".")
        self.position_label.config(text=f"Ln {position[0]}, Col {position[1]}")

class SearchArea(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master, pad=5)

        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1)

        self.previous_button = tk.Button(self, text="Prev", pady=1, command=lambda: self.search_text(self.entry.get()))
        self.previous_button.grid(row=0, column=2)

        self.next_button = tk.Button(self, text="Next", pady=1, command=lambda: self.search_text(self.entry.get()))
        self.next_button.grid(row=0, column=3)

        self.close_button= tk.Button(self, text="X", pady=1, padx=5, bg="grey50", fg="white", command=lambda: self.close())
        self.close_button.grid(row=0, column=4)

        self.entry.bind("<KeyRelease>", self.update)

    def close(self):
        self.grid_remove()
        global edit_area
        edit_area.text.tag_delete("found")

    def search_text(self, string):
        global edit_area

        edit_area.text.tag_delete("found")
    
        if string.strip() == "":
            return

        found_indexes = []

        s = string
        if s:
            idx = '1.0'
            while 1:
                idx = edit_area.text.search(s, idx, nocase=1, stopindex="end")
                if not idx: break
                found_indexes.append(idx)
                lastidx = '%s+%dc' % (idx, len(s))
                edit_area.text.tag_add('found', idx, lastidx)
                idx = lastidx
                edit_area.text.see(idx)  # Once found, the scrollbar automatically scrolls to the text
            edit_area.text.tag_config('found', foreground='red')

        if len(found_indexes) == 0:
            self.entry.config(background="salmon")

    def update(self, event):
        self.search_text(self.entry.get())

        if self.entry.get().strip() == "":
            self.entry.config(background="white")

class ReplaceArea(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.old_label = tk.Label(self, text="Old:")
        self.old_label.grid(row=0, column=0)
        self.old_entry = tk.Entry(self)
        self.old_entry.grid(row=0, column=1)

        self.new_label = tk.Label(self, text="New:")
        self.new_label.grid(row=1, column=0)
        self.new_entry = tk.Entry(self)
        self.new_entry.grid(row=1, column=1)

        self.close_button= tk.Button(self, text="X", pady=1, padx=5, bg="grey50", fg="white", command=lambda: self.grid_remove())
        self.close_button.grid(row=0, column=2)

        self.replace_button = tk.Button(self, text="Replace", command=lambda: self.replace_text(self.old_entry.get(), self.new_entry.get()))
        self.replace_button.grid(row=2, column=0, columnspan=3)

    def replace_text(self, old, new):
        if old.strip == "" or new.strip == "":
            return

        global edit_area
        text_contents = edit_area.text.get("1.0", "end")
        new_text_contents = text_contents.replace(old, new)
        edit_area.text.delete("1.0", "end")
        edit_area.text.insert("1.0", new_text_contents)

root = tk.Tk()
root.title("Notepad")
root.geometry("700x600")

setup_menu()

current_file_path = ""

edit_area = EditArea(root)
edit_area.grid(row=0, column=0, sticky="wnse")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

info_bar = InfoBar(root)
info_bar.grid(row=1, column=0, sticky="e", padx=15)

search_area = SearchArea(root)
search_area.grid(row=0, column=0, sticky="ne", padx=14, pady=2)
search_area.grid_remove()

replace_area = ReplaceArea(root)
replace_area.grid(row=0, column=0, sticky="ne", padx=14, pady=2)
replace_area.grid_remove()

root.bind("<Key>", lambda x: info_bar.update())
root.bind("<Control-s>", lambda x: save_file())
root.bind("<Control-f>", lambda x: open_search_area())
root.bind("<Control-r>", lambda x: replace_area.grid())

root.mainloop()