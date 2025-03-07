import time
import tkinter as tk
from classmodule import Project, ForkOpenGUI, CreateNewGUI
from funcmodule import json_to_dict

# file = "code/cycle2/config.json"
# data = json_to_dict(file)

# testing_project: Project = Project(**data)

# print(testing_project.getName())
# testing_project.setLastSaved()
# print(testing_project.getLastSaved())
# time.sleep(5)
# testing_project.setLastSaved()
# print(testing_project.getLastSaved())



root = tk.Tk()
app = ForkOpenGUI(root)
# app = CreateNewGUI(root)
root.mainloop()

