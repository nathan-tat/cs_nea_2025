import tkinter as tk
from tkinter import messagebox

from classmodule import InstallGUI, safety
from funcmodule import is_admin



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
    
    
    # fix whats going on here
    if safety:
        print("Program was exited safely")
    else:
        messagebox.showerror("Error", "You have not exited safely.")