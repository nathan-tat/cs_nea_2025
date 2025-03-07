import json
from tkinter import messagebox
import os

def json_to_dict(filename: str) -> dict:
    with open(filename, "r") as file:
        return json.load(file)
        
        
def check_valid_project_name(string: str) -> None:
    
    if len(string) == 0:
        raise ValueError("Project name cannot have length zero.")

    if len(string) > 32:
        raise ValueError("Project name length cannot exceed 32.")
    
    if string.strip() == "":
        raise ValueError("Project name cannot be empty.")


    allowed: list = list(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_+= ()"
    )
    
    for c in string:
        if c not in allowed:
            raise ValueError(f"Project name cannot contain character '{c}'.")

            
def check_valid_project_dir(string: str) -> None:
    if not os.path.isdir(string):
        raise ValueError("Not a directory.")