import ctypes
from github import Github, Repository, ContentFile
import os
import requests
from win32com.client import Dispatch

# the requirements.txt which has all the necessary pip libraries to run the program 
REQ: str = (
    "https://raw.githubusercontent.com"
    "/nathan-tat/cs_nea_2025/main/requirements.txt"
)

# path to repository
REPO_NAME: str = "nathan-tat/cs_nea_2025"

# directory from which the software will be installed from 
SW_DIR: str = "code/software"

# file that the shortcut will link to
# I dont actually know what to call it
FILE = r"\code\software\main.py"

admin_flag = True

def download(c: ContentFile, out: str):
    """ https://github.com/Nordgaren/Github-Folder-Downloader/tree/master """
    r = requests.get(c.download_url)
    output_path = f'{out}/{c.path}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        print(f'downloading {c.path} to {out}')
        f.write(r.content)


def download_folder(repo: Repository, folder: str, out: str, recursive: bool):
    """ https://github.com/Nordgaren/Github-Folder-Downloader/tree/master """
    contents = repo.get_contents(folder)
    for c in contents:
        if c.download_url is None:
            if recursive:
                download_folder(repo, c.path, out, recursive)
            continue
        download(c, out)


def is_admin() -> bool:
    """ Returns `True` iff the current program is being run as administrator, else `False`. 
    Works on Windows 10 v.22H2 as of 2024-05-10
    https://stackoverflow.com/q/130763
    """
    if admin_flag: return admin_flag
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
    """ Installs the necessary python libraries from a 'requirements.txt' stored  
    at 'url' using pip
    """
    # the command is 
    # pip install -r /path/to/req.txt
    
    os.system(f"py -m pip install -r {url}")


def create_shortcut(source: str, dest: str) -> None:
    """ Creates a file shortcut to source at dest 
    https://stackoverflow.com/a/60944178
    """
    
    target = source + FILE
    
    shell = Dispatch("WScript.Shell")    
    shortcut = shell.CreateShortCut(dest)
    shortcut.Targetpath = target
    
    shortcut.WorkingDirectory = source
    shortcut.save()
    
    print("Desktop shortcut created")