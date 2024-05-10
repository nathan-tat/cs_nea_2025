import fsspec
import os
from pathlib import Path
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog



def download_from_github(url: str, destination: str) -> None:
    """ Downloads a given GitHub folder from 'url' to the 'destination' directory """
    pass


def install_requirements(url: str) -> None:
    """ 
    Installs the necessary python libraries from a 'requirements.txt' stored  
    at 'url' using pip
    """
    pass



class App:
    def __init__(self, root):
        #setting title
        root.title("Installer")
        #setting window size
        width=305
        height=160
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        btn_cancel=tk.Button(root)
        btn_cancel["text"] = "Cancel"
        btn_cancel.place(x=20,y=110,width=70,height=25)
        btn_cancel["command"] = self.btn_cancel_command

        btn_install=tk.Button(root)
        btn_install["text"] = "Install"
        btn_install.place(x=210,y=110,width=70,height=25)
        btn_install["command"] = self.btn_install_command

        btn_browse=tk.Button(root)
        btn_browse["text"] = "Browse"
        btn_browse.place(x=200,y=60,width=79,height=30)
        btn_browse["command"] = self.btn_browse_command

        self.ent_dir=tk.Entry(root)
        self.ent_dir["justify"] = "left"
        self.ent_dir["text"] = "C:\\Program Files\\"
        self.ent_dir.place(x=20,y=60,width=183,height=30)

        self.lbl_welcome=tk.Label(root)
        self.lbl_welcome["justify"] = "center"
        self.lbl_welcome["text"] = "this is the installer"
        self.lbl_welcome.place(x=20,y=20,width=170,height=30)


    def btn_cancel_command(self) -> None:
        """ Closes the UI window safely. """
        print("Exiting...")
        root.destroy()


    def btn_install_command(self) -> None:
        """ Installs the software to the given directory. Probably very not secure. """
        target: str = self.filename
        


    def btn_browse_command(self) -> None:
        """ Allows the user to select a directory to install the software into. Check permissions. """
        self.filename = filedialog.askdirectory()
        # self.lbl_welcome["text"] = self.filename




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
