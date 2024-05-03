import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=300
        height=160
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        btn_cancel=tk.Button(root)
        btn_cancel["text"] = "Cancel"
        btn_cancel.place(x=10,y=110,width=70,height=25)
        btn_cancel["command"] = self.btn_cancel_command

        btn_init=tk.Button(root)
        btn_init["text"] = "Initialise"
        btn_init.place(x=100,y=110,width=70,height=25)
        btn_init["command"] = self.btn_init_command

        btn_open=tk.Button(root)
        btn_open["text"] = "Open"
        btn_open.place(x=190,y=110,width=70,height=25)
        btn_open["command"] = self.btn_open_command
        
        btn_browse = tk.Button(root)
        btn_browse["text"] = "Browse"
        btn_browse.place(x=220,y=70,width=70,height=25)
        btn_browse["command"] = self.btn_browse_command

        lbl_welcome=tk.Label(root)
        lbl_welcome["justify"] = "center"
        lbl_welcome["text"] = "welcome kind user"
        lbl_welcome.place(x=40,y=10,width=100,height=25)
        
        ent_directory=tk.Entry(root)
        ent_directory["text"] = "Entry"
        ent_directory.place(x=20,y=70,width=200,height=25)


    def btn_cancel_command(self):
        print("Successfully destroyed")
        root.destroy()


    def btn_browse_command(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        print(filename)
    

    def btn_init_command(self):
        print("initialise button !!")


    def btn_open_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
