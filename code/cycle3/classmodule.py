from funcmodule import *

import tkinter as tk
from tkinter import messagebox

from math import floor

# default size of the window
WIDTH = 1280
HEIGHT= 720
RIBBON_HEIGHT = 25
SPACING = 50
PADDING = 10

# this will be shared between GUI elements
# this is the configuration settings for the meters
global meter
meter: dict

class SimulatorGUI:
    def __init__(self, root: tk.Tk, name: str = None):
        # setting title
        
        root.title(name)
        self.name = name

        # setting window size
        w = WIDTH
        h = HEIGHT
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        self.root = root
        
        # frames
        components: tk.Frame = tk.Frame(
            root, width=300, height=HEIGHT-RIBBON_HEIGHT-PADDING, relief="groove", borderwidth=5
        )
        canvas: tk.Frame = tk.Frame(
            root, width=WIDTH-300, height=HEIGHT-RIBBON_HEIGHT-PADDING, relief="sunken", borderwidth=5
        )
        ribbon: tk.Frame = tk.Frame(
            root, width=WIDTH, height=RIBBON_HEIGHT+PADDING, relief="raised", borderwidth=5
        )
        
        # aligning them
        ribbon.pack(side="top")
        components.pack(side="left")
        canvas.pack(side="right")
        
        # how many buttons per row
        self.countx = floor((WIDTH-300)/SPACING)
        # how many buttons in a column
        self.county = floor((HEIGHT-RIBBON_HEIGHT)/SPACING)
        
        # the index of the button
        # from this value you can calculate where on the canvas the button is
        index = 0
        
        dx = 10
        dy = 10
        
        self.lattice: list[tk.Button] = []
        
        # fill out rows first then columns
        for j in range(self.county):
            for i in range(self.countx):
                x = SPACING * (i + 1) - dx
                y = SPACING * (j + 1) - dy
                
                # thank you 
                # https://stackoverflow.com/a/10865170
                
                self.button = tk.Button(
                    canvas, bg="black",
                    command=lambda index=index: self.lat_button_command(index)
                )
                
                self.button.place(
                    x=x, y=y, height=dx, width=dy
                )
                
                self.lattice.append(self.button)
                
                index += 1
                
                
        # i need to place the buttons for the components 
        
        self.names: list[str] = [
            "Ammeter",
            "Wire",
            "Cell",
            "Resistor",
            "Bulb"
        ]
        
        self.componentButtons: list[tk.Button] = []
        
        component_height = 100
        # placing these iteratively as well
        for n in range(len(self.names)):
            x = PADDING
            y = n * (component_height + PADDING) + PADDING
            text = self.names[n]
            # print(text)
            
            # the text is now working
            self.button = tk.Button(
                components, text=text,
                command=lambda n=n: self.component_button_command(n)
            )
            
            self.button.place(
                x=x, y=y, height=component_height, width=300-2*PADDING
            )
            
            self.componentButtons.append(self.button)
            
            
            
        # placing in save/quit buttons
        
        # save button
        btnSave = tk.Button(
            ribbon, text="Save", command=self.save
        )
        btnSave.place(
            x=0, y=0, width=100
        )
        
        # exit button
        btnExit = tk.Button(
            ribbon, text="Quit", command=self.quit
        )    
        btnExit.place(
            x=100+PADDING, y=0, width=100
        )
        
        # run button
        btnRun = tk.Button(
            ribbon, text="Run", command=self.run
        )
        btnRun.place(
            x=200+2*PADDING, y=0, width=100
        )
        
        # reset button
        btnReset = tk.Button(
            ribbon, text="Reset", command=self.reset
        )
        btnReset.place(
            x=300+3*PADDING, y=0, width=100
        )
        
        
        # flags for later
        
        self.active = False
        self.pos = tk.IntVar()
        self.neg = tk.IntVar()
        self.count = 0
        
        self.pos.set(-1)
        self.neg.set(-1)
        
        # this is the whole circuit
        self.circuit: dict = {}

        
    def lat_button_command(self, index):
        """ Return which order the button was placed """
        if not self.active:
            print("Inactive")
            return
        
        print("active")
        print(index)
        
        if self.pos.get() == -1:
            self.pos.set(index)
            return
        
        # dont want to select the same one twice
        if self.pos.get() == index:
            return
        
        if self.neg.get() == -1:
            self.neg.set(index)
            return
        
    def component_button_command(self, index):
        # have to finish placing this component before can place another
        if self.active:
            print("Button already active")
            return
        
        # setting the flag
        self.active = True
        
        # if its an ammeter
        global meter
        if index == 0:
            app2 = MeterGUI(self.root)
        else:
            meter = {}
        
        # wait for the second lattice point to be clicked
        self.root.wait_variable(self.neg)
        
        component: dict = {
            "type": self.names[index].lower(),
            "pos": self.pos.get(),
            "neg": self.neg.get(),
            "data": meter
        }
        
        # reset flags
        self.pos.set(-1)
        self.neg.set(-1)
        self.active = False
        
        self.circuit[str(self.count)] = component
        
        self.count += 1
        
        print(self.circuit)
        
    def save(self):
        # this method converts the bad self.component and writes 
        # the proper one to the json file
        print("saving...")
        
        jsonCircuit: dict = {}
        
        for i in range(self.count):
            # this will have pos, neg, type, and data
            current = {}
            
            # convert to string to get the key
            k = str(i)
            
            # finding positive terminal connection
            pos = self.circuit[k]["pos"]
            single = 0
            for j in range(self.count):
                # skip self
                if i == j: continue
                l = str(j)
                
                # check if connected to the component
                if (self.circuit[l]["pos"] == pos 
                        or self.circuit[l]["neg"] == pos):
                    current["pos"] = j
                    single += 1
                
            # raise error if no connection or 
            # if there are too many connections
            if single == 0:
                messagebox.showerror(
                    "No connection !!", 
                    "No connection found, redo circuit"
                )
                self.reset()
                return
            
            if single != 1:
                messagebox.showerror(
                    "Too many connections", 
                    "Too many connections to one point",
                )
                self.reset()
                return
            
            
            # finding negative terminal connection
            neg = self.circuit[k]["neg"]
            single = 0
            for j in range(self.count):
                if i == j: continue
                l = str(j)
                
                # check if connected to neg terminal
                if (self.circuit[l]["pos"] == neg or 
                        self.circuit[l]["neg"] == neg):
                    current["neg"] = j
                    single += 1
                    
            # raise error if not found or if too many found
            if single == 0:
                messagebox.showerror(
                    "No connection !!", 
                    "No connection found, redo circuit"
                )
                self.reset()
                return
            
            if single != 1:
                messagebox.showerror(
                    "Too many connections", 
                    "Too many connections to one point",
                )
                self.reset()
                return
            
            
            # add type and data and add to main
            current["type"] = self.circuit[k]["type"]
            current["data"] = self.circuit[k]["data"]

            jsonCircuit[k] = current
            
        # write dictionary to json file
        dict_to_json(jsonCircuit, "circuit.json")
        
        print("Finished saving")
    
    def quit(self):
        print("exiting....")
        self.root.destroy()

        
    def run(self):
        print("Running program ... ")
        
        # grab circuit as a python dictionary        
        circuit = json_to_dict("circuit.json")

        # checking for ammeters
        for k in circuit.keys():
            if "meter" in circuit[k]["type"]:
                break
        else:
            # no meters so no work :p
            messagebox.showinfo(
                "No meters found",
                "No meters have been found in the circuit"
            )
            return
        
        # this holds info about components e.g. resistance 
        data: dict = json_to_dict("data.json")
        
        # total resistance of circuit
        # using V = ir
        total_res: float = 0
        total_emf: float = 0
        
        for k in circuit.keys():
            type = circuit[k]["type"]
            
            res = data[type]["resistance"]
            emf = data[type]["emf"]

            total_emf += emf
            total_res += res
            
        # this is the total current in the circuit
        # rearranging ohm's law
        current = total_emf/total_res if total_res > 0 else "infinity"
        # every ammeter is reading the same thing
        
        
        # looping over stuff again
        # and creating another dictionary on top of that
        readings: dict = {
            "emf": total_emf,
            "resistance": total_res,
            "ameters": [],
            # "vmeters": [] not yet implemented
        }
        
        for k in circuit.keys():
            # ignore non-meters
            if "meter" not in circuit[k]["type"]:
                continue
            
            # copy over data
            m: dict = circuit[k]["data"]
            # measured in amps
            m["current"] = current
            
            readings["ameters"].append(m)
            
        app = OutputGUI(self.root, readings)
        
        
        print("Finished running")
            
        
        
    def reset(self):
        self.circuit = {}
        self.count = 0
        print("Circuit cleared")


class OutputGUI(tk.Toplevel):
    def __init__(self, master: tk.Tk, readings: dict):
        super().__init__(master=master)
        
        w = 350
        h = 250
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.title("Meter output")
        
        # for alignment purposes
        maxLen = 35 # characters
        
        # showing total emf 
        totalEMF = readings["emf"]
        strVal = str(totalEMF) + " V"
        
        text = normaliseString(
            "Total E.M.F.", strVal, maxLen
        )

        lblEMF = tk.Label(
            self, text=text, font="TkFixedFont"
        )
        lblEMF.place(
            x=PADDING, y=PADDING
        )
        
        # showing total resistance
        totalRes = readings["resistance"]
        strVal = str(totalRes) + " W"

        text = normaliseString(
            "Total resistance", strVal, maxLen
        )

        lblRes = tk.Label(
            self, text=text, font="TkFixedFont"
        )
        lblRes.place(
            x=PADDING, y=15+2*PADDING
        )
        
        for i, m in enumerate(readings["ameters"]):
            # the reading and id
            val = m["current"]
            
            if val != "infinity":
                # adjusting reading for prefix
                if m["units"] == "kA":
                    val /= 10**3
                elif m["units"] == "mA":
                    val *= 10**3
                elif m["units"] == "uA":
                    val *= 10**6
                    
                # getting the value rounded
                precision = m["res"]
                strVal = round_sig_fig(val, precision) + " " + m["units"]
            else:
                strVal = val
            
            text = normaliseString(
                m["id"], strVal, maxLen
            )
                
            # create label
            lblId = tk.Label(
                self, text=text, font="TkFixedFont"
            )
            lblId.place(
                x=PADDING, y=(i+2)*(15+PADDING)+2*PADDING
            )



class MeterGUI(tk.Toplevel):
    def __init__(self, root: tk.Tk):
        # so that it can run from the main window        
        super().__init__(master=root)
        
        # setting window size
        w = 350
        h = 200
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.title("Meter configuration")
        


        # identifier
        self.lblId = tk.Label(
            self, text="Identifier:"
        )
        self.lblId.place(
            x=PADDING, y=PADDING
        )
        # validation
        vid = (self.register(validateIdentifier))
        
        self.entID = tk.Entry(
            self, validate="all", validatecommand=(vid, "%P")
        )
        self.entID.place(
            x=PADDING, y=2*PADDING +10, width=350-2*PADDING
        )
        
        
        # units dropdown
        self.lblUnits = tk.Label(
            self, text="Units:"
        )
        self.lblUnits.place(
            x=PADDING, y=3*PADDING+20
        )
        
        # options
        units = [
            "kA",
            " A",
            "mA",
            "uA",
        ]
        self.value = tk.StringVar(self)
        self.value.set("Select units")
        self.menUnits = tk.OptionMenu(
            self, self.value, *units
        )
        self.menUnits.place(
            x=PADDING, y=4*PADDING+30, width=350-2*PADDING
        )
        
        
        # resolution
        self.lblResolution = tk.Label(
            self, text="Resolution (significant figures):"
        )
        self.lblResolution.place(
            x=PADDING, y=5*PADDING+60
        )
        
        # validation function
        vres = (self.register(validateResolution))
        
        self.entResolution = tk.Entry(
            self, validate="all", validatecommand=(vres, "%P")
        )
        self.entResolution.place(
            x=PADDING, y=6*PADDING+70, width=350-2*PADDING
        )
        
        
        # create button
        self.btnCreate = tk.Button(
            self, text="Create", command=self.btnCreateCommand
        )
        
        self.btnCreate.place(
            x=350-100-PADDING, y=200-30-PADDING, width=100, height=30
        )
        
    def btnCreateCommand(self):
        global meter

        # reset
        meter = {}
        
        # dont do anything if any of them havent been selected
        if self.value.get() == "Select units":
            return
        
        # strip to catch spaces
        if self.entID.get().strip() == "":
            return
        
        if self.entResolution.get() == "":
            return
        
        
        # putting it into the dictionary
        # this is global !!! (to share with the other user interface)
        meter = {
            "id": self.entID.get(),
            "units": self.value.get(),
            "res": int(self.entResolution.get())
        }
        
        # print(meter)
        
        self.destroy()