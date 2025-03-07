""" 
Implement UI like shown in design
Implement Project class that does a bunch of stuff
"""
import shutil
import time
import tkinter as tk
import json
import os
from tkinter import filedialog
from tkinter import messagebox

from funcmodule import check_valid_project_name, check_valid_project_dir, json_to_dict


class Project:
    def __init__(
        self, 
        directory: str, 
        name: str, 
        type: str,
        created: int, 
        lastSaved: int
    ) -> None:
        
        self.__name: str = name
        self.__created: int = created
        self.__lastSaved: int = lastSaved
        self.__directory: str = directory
        self.__type: int = type
        
        # the maximum length for a project name
        self.maxNameLength = 32
        
        
    def setName(self, name: str) -> None:
        """ Sets the name attribute of the project, along with validation.
        \nRaises `ValueError` if `name` exceeds `maxNameLength`"""
        
        err = "'name' is too long "
        err += f"(received {len(name)}, expected <= {self.maxNameLength})."
        if len(name) > self.maxNameLength:
            raise ValueError(err)
        
        self.__name = name
    
    def getName(self) -> str:
        """ Returns name """
        return self.__name
    
    
    def setLastSaved(self) -> None:
        """ Sets the `lastSaved` time to the current UNIX timestamp
        to the nearest second """
        self.__lastSaved = round(time.time())
        
    def getLastSaved(self) -> int:
        """ Returns `lastSaved` """
        return self.__lastSaved
    
    
    def getType(self) -> str:
        """ Returns `type` """
        return self.__type
    
    
    def getCreated(self) -> int:
        """ Returns `created` """
        return self.__created
    
    
    def save(self) -> None:
        
        # will also need this to write to q.txt
        self.setLastSaved()
        self.configUpdate()
    
    
    def export(self, destination: str) -> None:
        """ Saves the directory of the project as a .zip 
        file to a given destination
        """
        # https://stackoverflow.com/a/25650295
        shutil.make_archive(self.__name, "zip", self.__directory, destination)
    
    
    def open(self) -> None:
        print(f"Opening '{self.__name}'...")
    
    
    def close(self) -> None:
        pass
    
    
    def configUpdate(self) -> None:
        """ Updates the config file to latest settings """
        # target json file to write to  
        filename: str = self.__directory + "\\config.json"

        data: dict = {
            "directory": self.__directory,
            "name": self.__name,
            "type": self.__type,
            "created": self.__created,
            "lastSaved": self.__lastSaved
        }
        
        with open(filename, "w") as file:
            json.dump(data, file)
    
    # I think I would like to do some more on this

class FileQueue:
    def __init__(self, location: str, maxLength: int = 3):
        self.__maxLength = maxLength
        self.__location = location
        
        self.__front = 0
        self.__rear = 0
        
        # counting the length to set the rear pointer. 
        # this needs to be set every time this is initially opened
        with open(location, "r") as file:
            for i in file:
                self.__rear += 1
                
        # decrement by 1 to make it 0 indexed
        self.__rear -= 1
                
        # if the file has less than maxLength lines
        if self.__rear <= maxLength:
            self.__front = 0
        else:
            self.__front = self.__rear - maxLength + 1
            

        
    def length(self) -> int:
        """ Returns the amount of the elements in the `FileQueue` """
        return self.__rear - self.__front + 1
        
        
    def deq(self) -> str:
        """ Increments the `front` pointer and returns the element at the front of the `FileQueue` """
        
        # if the queue is empty raise an exception
        if self.length() == 0:
            raise Exception("Queue Underflow")
        
        value = ""
        
        with open(self.__location, "r") as file:
            value = file.readlines()[self.__front]
            

        self.__front += 1
        
        # stripped to remove whitespace
        return value.strip()
    
    
    def enq(self, projectDir: str) -> None:
        """ Adds an item to the back of the `FileQueue` """
        # append the new project to the file
        # this happens regardless of pointers
        with open(self.__location, "a") as file:
            file.write(projectDir + "\n")
        
        
        # pointer logic
        # if the file has enough elements to be considered "full"
        if self.length() == self.__maxLength:
                
            # update front and rear pointers
            self.__rear += 1
            self.__front += 1
        
        else:
            
            # front does not always need to be considered  
            # eg maxLength = 4, rear = 1, front = 0
            # incrementing rear and front results 
            # in a queue of length 2 still (but should be 3)
            
            self.__rear += 1
            
        # my only gripe with this implementation is that it allows for duplicates
            
            
    def drop(self) -> list:
        """ Returns all the elements in the `FileQueue as a list """
        temp = []
        
        # if it is empty return an empty list
        if self.length() == 0:
            return temp
        
        
        # read from the file
        with open(self.__location, "r") as file:
            # problem with calling "file.readlines()" repeatedly
            lines = file.readlines()
            for i in range(self.__front, self.__rear + 1):
                # print(i)
                temp.append(lines[i].strip())
                
        return temp

# button 1 (cancel, etc.)
BTN1_W = 100
BTN1_H = 30
# button 2 (special ones)
BTN2_W = 250
BTN2_H = 40
# window
WIDTH = 400
HEIGHT = 200
# padding
PAD = 10

QUEUE = "q.txt"

# yeah so ill have 1 instance of FileQueue and 3 instances of project
# i need to show that the thing with reading from json files into an object works
# ill do that later. 

class ForkOpenGUI:
    def __init__(self, root: tk.Tk):
        # setting title
        root.title("Open project")

        # setting window size
        w = WIDTH
        h = HEIGHT
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        self.root = root
        
        # `Recently Viewed` label
        self.lbl_info1 = tk.Label(
            root, justify="left", text="Recently viewed:"
        )
        self.lbl_info1.place(
            x=PAD, y=PAD, width=100, height=BTN1_H
        )

        
        # Cancel button
        self.btn_cancel = tk.Button(
            root, text="Cancel", command=self.btn_cancel_command
        )
        self.btn_cancel.place(
            x=WIDTH-PAD-BTN1_W, y=HEIGHT-PAD-BTN1_H, width=BTN1_W, height=BTN1_H
        )
        
        # Open New button
        self.btn_open_new = tk.Button(
            root, text="Open new", command=self.btn_open_new_command
        )
        self.btn_open_new.place(
            x=WIDTH-PAD-BTN1_W, y=PAD, width=BTN1_W, height=BTN1_H
        )
        
        # Open Existing button
        self.btn_open_exist = tk.Button(
            root, text="Open existing", command=self.btn_open_exist_command
        )
        self.btn_open_exist.place(
            x=WIDTH-PAD-BTN1_W, y=PAD+PAD+BTN1_H, width=BTN1_W, height=BTN1_H
        )
        
        # getting the most recent projects
        q: FileQueue = FileQueue("code\\cycle2\\q.txt")

        self.projects: list[Project] = []
        
        for i in range(q.length()):
            self.projects.append(
                Project(**json_to_dict(q.deq()))
            )
                
        # now setting up the dynamic ones
        # project 1
        self.btn_project1 = tk.Button(
            root, text="-", command=self.btn_project1_command, state="disabled"
        )
        
        try:
            self.btn_project1["text"] = self.projects[0].getName()
            self.btn_project1["state"] = "active"
            
        except IndexError:
            pass
        
        finally:
            self.btn_project1.place(
                x=PAD, y=2*PAD+BTN1_H, width=BTN2_W, height=BTN2_H
            ) 
        
        
        # project 2
        self.btn_project2 = tk.Button(
            root, text="-", command=self.btn_project2_command, state="disabled"
        )
        
        try:
            self.btn_project2["text"] = self.projects[1].getName()
            self.btn_project2["state"] = "active"
            
        except IndexError:
            pass
        
        finally:
            self.btn_project2.place(
                x=PAD, y=3*PAD+BTN1_H+BTN2_H, width=BTN2_W, height=BTN2_H
            )
            
            
        # project 3
        self.btn_project3 = tk.Button(
            root, text="-", command=self.btn_project3_command, state="disabled"
        )
        
        try:
            self.btn_project3["text"] = self.projects[2].getName()
            self.btn_project3["state"] = "active"
            
        except IndexError:
            pass
        
        finally:
            self.btn_project3.place(
                x=PAD, y=4*PAD+BTN1_H+2*BTN2_H, width=BTN2_W, height=BTN2_H
            )
            
        



    def btn_cancel_command(self) -> None:
        print("Exiting....")
        self.root.destroy()
    
    def btn_open_new_command(self) -> None:
        """ Links the user to another GUI and allows them to create a project """
        print("Open new")
        self.root.destroy()
        
        # open the other GUI for creating new projects
        newRoot = tk.Tk()
        newApp = CreateNewGUI(newRoot)
        newRoot.mainloop()
        
    
    def btn_open_exist_command(self) -> None:
        """ Allows the user to select a config file
        from which a project will be opened """
        
        config: str = filedialog.askopenfilename(
            filetypes=[("JSON file", ".json")]
        )
        print(config)
        
        # if a file has been selected
        if config:
            self.root.destroy()
        

        
    def btn_project1_command(self) -> None:
        self.root.destroy()
        self.projects[0].open()

    def btn_project2_command(self) -> None:
        self.root.destroy()
        self.projects[1].open()

    def btn_project3_command(self) -> None:
        self.root.destroy()
        self.projects[2].open()
        
        
        
ENT_H = 25
        
class CreateNewGUI:
    def __init__(self, root: tk.Tk):
        # setting title
        root.title("Create new project")
        
        # setting window sizes
        w = WIDTH
        h = HEIGHT
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.root = root
        
        # Project Name
        # label
        self.lblName = tk.Label(
            root, justify="left", text="Project name:"
        )
        self.lblName.place(
            x=PAD, y=PAD, width=75, height=ENT_H
        )
        
        # entry
        self.entName = tk.Entry(root)
        self.entName.place(
            x=PAD, y=2*PAD+ENT_H, width=WIDTH-PAD-PAD, height=BTN1_H 
        )
        
        # Directory
        # label
        self.lblDir = tk.Label(
            root, justify="left", text="Project folder:"
        )
        self.lblDir.place(
            x=PAD, y=3*PAD+BTN1_H+ENT_H, width=75, height=ENT_H
        )
        
        # showing user the directory they chose
        self.entDir = tk.Entry(root)
        self.entDir.place(
            x=PAD, y=4*PAD+BTN1_H+2*ENT_H, width=WIDTH-PAD-PAD-BTN1_W, height=BTN1_H,
        )
        
        # browse button
        self.btnBrowse = tk.Button(
            root, text="Browse", command=self.btnBrowseCommand
        )
        self.btnBrowse.place(
            x=WIDTH-PAD-BTN1_W, y=4*PAD+BTN1_H+2*ENT_H, width=BTN1_W, height=BTN1_H
        )
        
        # cancel button
        self.btnCancel = tk.Button(
            root, text="Cancel", command=self.btnCancelCommand
        )
        self.btnCancel.place(
            x=PAD, y=HEIGHT-PAD-BTN1_H, width=BTN1_W, height=BTN1_H
        )
        
        # create button
        self.btnCreate = tk.Button(
            root, text="Create", command=self.btnCreateCommand, state="disabled"
        )
        self.btnCreate.place(
            x=WIDTH-PAD-BTN1_W, y=HEIGHT-PAD-BTN1_H, width=BTN1_W, height=BTN1_H
        )
        
        # type
        # no clue how to do a drop down i wont even lie
        # i might just drop this completely
        
        # the variables needed for l8r 
        self.projectName: str
        self.projectDir: str


    def btnBrowseCommand(self) -> None:
        """ 
        Allows the user to select a directory to install the software into. 
        Check permissions. 
        """
        self.projectDir = filedialog.askdirectory()
        
        # this line was missing
        self.entDir.delete(0, tk.END)
        
        self.entDir.insert(0, self.projectDir)
        
        self.btnCreate["state"] = "active"
        
    
    def btnCancelCommand(self) -> None:
        """ Exits out of the user interface """
        print("Exiting...")
        self.root.destroy()
        
        
    def btnCreateCommand(self) -> None:
        """ This writes the options to a json file somewhere """
        
        try:
            
            # this is what will be written to the json file somewhere 
            data: dict = {}        
            
            # getting the name 
            self.projectName = self.entName.get()
            
            try:
                check_valid_project_name(self.projectName)
            except ValueError as e:
                messagebox.showerror("Error", e)
                print(self.projectName)
                return
            else:
                data["name"] = self.projectName
                

            # getting the directory
            self.projectDir = self.entDir.get()
            
            try:
                check_valid_project_dir(self.projectDir)
            except ValueError as e:
                messagebox.showerror("Error", e)
                print(self.projectDir)
                return
            else:
                data["directory"] = self.projectDir
                

            # setting `type` to none
            data["type"] = None
            

            # setting `created` and `lastSaved` using current time
            now = round(time.time())

            data["created"] = now
            data["lastSaved"] = now
            
    
            # writing to the file
            configFile = self.projectDir + "\\config.json"

            with open(configFile, "w") as file:
                json.dump(data, file)
                
    
        except Exception as e:
            # catching any other errors and displaying them to the user
            messagebox.showerror("Error", e)
        
        else:
            # if no exceptions are caught
            messagebox.showinfo(
                "Success!", 
                f"Successfully created '{self.projectName}' in '{self.projectDir}'"
            )
            
            self.root.destroy()
            
            project = Project(**data)
            project.open()
            
    