import ctypes
from github import Github, Repository, ContentFile
import os
import sys
import requests
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import messagebox

# if im testing stuff 
testing = True


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


""" 
^^^ End of code from https://github.com/Nordgaren/Github-Folder-Downloader/tree/master
"""


# the requirements.txt which has all the necessary pip libraries to run the program 
REQ: str = "https://raw.githubusercontent.com/nathan-tat/cs_nea_2025/main/requirements.txt"
# path to repository
REPO_NAME: str = "nathan-tat/cs_nea_2025"
# directory from which the software will be installed from 
SW_DIR: str = "code/software"

safety = False


# thank you stackoverflow
# https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
def is_admin() -> bool:
    """
    Returns 'True' iff the current program is being run as administrator, else 'False'. 
    Works on Windows 10 v.22H2 as of 2024-05-10
    """
    if testing: return testing
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
    # i dont think this actually works as of now
    # os.system(f"py -m pip install {url}")
    pass


class InstallGUI:
    def __init__(self, root):
        #setting title
        root.title("Installer")
        #setting window size
        w = 305
        h = 160
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.btn_cancel = tk.Button(root)
        self.btn_cancel["text"] = "Cancel"
        self.btn_cancel.place(x=20,y=110,width=70,height=25)
        self.btn_cancel["command"] = self.btn_cancel_command

        self.btn_install = tk.Button(root)
        self.btn_install["text"] = "Install"
        self.btn_install.place(x=210,y=110,width=70,height=25)
        self.btn_install["command"] = self.btn_install_command
        self.btn_install["state"] = "disabled"

        self.btn_browse = tk.Button(root)
        self.btn_browse["text"] = "Browse"
        self.btn_browse.place(x=200,y=60,width=79,height=30)
        self.btn_browse["command"] = self.btn_browse_command

        self.lbl_dir = tk.Label(root)
        self.lbl_dir["justify"] = "left"
        self.lbl_dir["text"] = "Install Directory" # initial text
        self.lbl_dir.place(x=20,y=60,width=183,height=30)

        self.lbl_welcome = tk.Label(root)
        self.lbl_welcome["justify"] = "center"
        self.lbl_welcome["text"] = "This is the installer."
        self.lbl_welcome.place(x=20,y=20,width=170,height=30)
        
        self.filepath = None


    def btn_cancel_command(self) -> None:
        """ Closes the UI window safely """
        global safety
        safety = True
        print("Exiting...")
        root.destroy()


    def btn_install_command(self) -> None:
        """ 
        Installs the software to the given directory. 
        Probably very not secure. 
        """
        # set it equal to eachother 
        if self.filepath != self.lbl_dir["text"]:
            self.filepath = self.lbl_dir["text"]
            
        # if not a real directory
        if not os.path.isdir(self.filepath):
            pass
        
        # do some fancy stuffs
        # like turning off some of the buttons
        self.btn_browse["state"] = "disabled"
        self.btn_cancel["state"] = "disabled"
        self.btn_install["state"] = "disabled"
        
        self.lbl_welcome["text"] = "Please wait... Downloading..."
        
        if not testing:
            # this probably works
            try:
                install_requirements(REQ)
                download_from_github(self.filepath)
                
            except Exception as e:
                # if something goes wrong then output the exception that was raised
                self.lbl_welcome["text"] = f"something bad happened: {e}"
            else:
                # if everything goes fine
                self.lbl_welcome["text"] = f"Installed to {self.lbl_dir['text']}"
        else:
            self.lbl_welcome["test"] = f"Installed to {self.lbl_dir['text']}"
        
        self.btn_browse["state"] = "active"
        self.btn_cancel["state"] = "active"
        self.btn_install["state"] = "active"
        

    def btn_browse_command(self) -> None:
        """ Allows the user to select a directory to install the software into. Check permissions. """
        self.filepath = filedialog.askdirectory()
        # self.lbl_welcome["text"] = self.filepath
        self.lbl_dir["text"] = self.filepath
        self.btn_install["state"] = "active"


if __name__ == "__main__":
    if not is_admin():
    #     # brings up UAC pop-up
    #     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        
    #     # if the user denied admin privilages
    #     if not is_admin():
    #         # this doesn't work 
    #         raise PermissionError("Program is not being run as Administrator")
        raise Exception("You are not admin.")
        
    root = tk.Tk()
    app = InstallGUI(root)
    root.mainloop()
    
    if safety:
        print("Program was exited safely")
    else:
        messagebox.showerror("Error", "You have not exited safely.")