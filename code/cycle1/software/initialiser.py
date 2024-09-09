""" 
This is going to run the GUI where you can choose to open/init a project
neato
"""

import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog


def open_folder(dir: str) -> None:
    """ 
    This is going to run the main program using the directory as an argument
    Not implemented as of 2024-05-27
    """
    return
    

def check_valid_dir(dir: str) -> bool:
    """ 
    Checks if a directory has a config file in it (ie is a project that has been initialised) 
    """
    # needs to be a valid directory
    if not os.path.isdir(dir): return False

    # im literally just going to check whether or not the folder contains a json file
    for f in os.listdir(dir):
        # in case of invalid index errors
        if not len(f) < 5:
            if f[-4] == "json":
                return True
    else:
        return False


class OpenGUI:
    def __init__(self, root):
        #setting title
        root.title("Opener")
        #setting window size
        w = 305
        h = 160
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (w, h, (sw - w)/2, (sh - h) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.btn_cancel = tk.Button(root)
        self.btn_cancel["text"] = "Cancel"
        self.btn_cancel.place(x=20,y=110,width=70,height=25)
        self.btn_cancel["command"] = self.btn_cancel_command

        self.btn_open = tk.Button(root)
        self.btn_open["text"] = "Open"
        self.btn_open.place(x=210,y=110,width=70,height=25)
        self.btn_open["command"] = self.btn_open_command
        self.btn_open["state"] = "disabled"

        self.btn_browse = tk.Button(root)
        self.btn_browse["text"] = "Browse"
        self.btn_browse.place(x=200,y=60,width=79,height=30)
        self.btn_browse["command"] = self.btn_browse_command

        self.ent_dir = tk.Entry(root)
        self.ent_dir["justify"] = "left"
        self.ent_dir.place(x=20,y=60,width=183,height=30)

        self.lbl_welcome = tk.Label(root)
        self.lbl_welcome["justify"] = "center"
        self.lbl_welcome["text"] = "this is the opener"
        self.lbl_welcome.place(x=20,y=20,width=170,height=30)
        
        self.filepath = None


    def btn_cancel_command(self) -> None:
        """ Closes the UI window safely """
        print("Exiting...")
        root.destroy()


    def btn_open_command(self) -> None:
        if not check_valid_dir(self.filepath):
            raise Exception("Invalid thing")
        open_folder(self.filepath)
            

    def btn_browse_command(self) -> None:
        """ Allows the user to select a directory to open """
        self.filepath = filedialog.askdirectory()
        self.lbl_welcome["text"] = self.filepath
        self.ent_dir["text"] = self.filepath
        self.btn_open["state"] = "active"
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = OpenGUI(root)
    root.mainloop()
