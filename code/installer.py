import ctypes
from github import Github, Repository, ContentFile
import os
import sys
import requests
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog


""" 
The following code downloads a folder from GitHub
Source: https://github.com/Nordgaren/Github-Folder-Downloader/tree/master
"""


def download(c: ContentFile, out: str):
    r = requests.get(c.download_url)
    output_path = f'{out}/{c.path}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        print(f'downloading {c.path} to {out}')
        f.write(r.content)


def download_folder(repo: Repository, folder: str, out: str, recursive: bool):
    contents = repo.get_contents(folder)
    for c in contents:
        if c.download_url is None:
            if recursive:
                download_folder(repo, c.path, out, recursive)
            continue
        download(c, out)


def download_file(repo: Repository, folder: str, out: str):
    c = repo.get_contents(folder)
    download(c, out)


""" 
^^^ End of code from https://github.com/Nordgaren/Github-Folder-Downloader/tree/master
"""


# the requirements.txt which has all the necessary pip libraries to run the program 
REQ: str = "https://raw.githubusercontent.com/nathan-tat/cs_nea_2025/main/requirements.txt"
REPO_NAME: str = "nathan-tat/cs_nea_2025"
SW_DIR: str = "code/software"


def is_admin() -> bool:
    """
    Returns 'True' iff the current program is being run as administrator, else 'False'. 
    \nWorks on Windows 10 v.22H2 as of 2024-05-10
    \nhttps://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def download_from_github(destination: str) -> None:
    """ Downloads a given GitHub folder from 'url' to the 'destination' directory """
    g = Github()
    repo = g.get_repo(REPO_NAME)
    download_folder(repo, SW_DIR, destination, True)


def install_requirements(url: str) -> None:
    """ 
    Installs the necessary python libraries from a 'requirements.txt' stored  
    at 'url' using pip
    """
    os.system(f"py -m pip install {url}")



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
    if not is_admin():
        # brings up UAC pop-up
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        
        # if the user denied admin privilages
        if not is_admin():
            raise PermissionError("Program is not being run as Administrator")
        
    root = tk.Tk()
    app = App(root)
    root.mainloop()
