import tkinter as tk #window
from tkinter import ttk #labels - themed tk : ttk
from tkinter import *

class Project(object):
    win = tk.Tk() #instantiation 

    sen = 0
    startat= 50
    version = 2.1
    def __init__(self, title):
        self.title  = title
    def window(self):
        """create window
        """
        version = 2.1
        Project.win.title(self.title)
        #Project.win.resizable(0,0) #disable resizing the window
        ttk.Label(Project.win, text="Get DC Offset Program. Version: "+str(version),anchor="center").grid(column=0, row=0)

        label1 = ttk.Label(text="Sensitivity (default 35000):").grid(column=1,row=2)
        w1 = Scale(Project.win, from_=0, to=200000,orient=HORIZONTAL)#.grid(column=0,row=3,columnspan=3, sticky = tk.W+tk.E)
        w1.set(40000)
        w1.grid(column=0,row=3,columnspan=3, sticky = tk.W+tk.E)#.pack()
        
        button1 = ttk.Button(Project.win, text="Get DC all phases", command=lambda: self.instruction(1,w1)).grid(column=1,row=4)
        button6 = ttk.Button(Project.win, text="Get DC all phases second set", command=lambda: self.instruction(6,w1)).grid(column=1,row=5)
        button2 = ttk.Button(Project.win, text="Get DC for Red phase", command=lambda: self.instruction(2,w1)).grid(column=0,row=1)
        button3 = ttk.Button(Project.win, text="Get DC for White phase", command=lambda: self.instruction(3,w1)).grid(column=1,row=1)
        button4 = ttk.Button(Project.win, text="Get DC for Blue phase", command=lambda: self.instruction(4,w1)).grid(column=2,row=1)
        #ttk.Label(Project.win, text="Impedance Plot for PH-G only",anchor="center").grid(column=1, row=3)
        #button5 = ttk.Button(Project.win, text="Quick full impedance Plot", command=lambda: self.instruction(5)).grid(column=1,row=4)
        button10 = ttk.Button(Project.win, text="Terminate", command=lambda: Project.win.destroy()).grid(column=1,row=8)
        #button4 = ttk.Button(Project.win, text="Choose CFG", command=lambda: self.runcfg()).grid(column=3,row=1)
        
        
        
        Project.win.mainloop()

    #def runcfg(self):
    #    import roc_Fautldet_alltogetherImportClass#('A')
    def Set_Sens(self,w1):
        self.sen =  w1.get()
        print("Sensitivity is:", self.sen)
    
    def compute_A(self):
        #print("Sensitivity to calc ALL DC is:",self.sen)
        from DCRUNclass import DCRUNclass
        dd = DCRUNclass('all',self.sen,start=self.startat)
        #print("Run Code A")
    
    def compute_B(self):
        from DCRUNclass import DCRUNclass
        dd = DCRUNclass('r',self.sen,start=self.startat)
        #print("Run Code B")
    
    def compute_C(self):
        from DCRUNclass import DCRUNclass
        dd = DCRUNclass('w',self.sen,start=self.startat)
        #print("Run Code C")
        
    def compute_D(self):
        from DCRUNclass import DCRUNclass
        dd = DCRUNclass('b',self.sen,start=self.startat)
        #print("Run Code C")

    def compute_E(self):
        from DCRUNclass import DCRUNclass
        dd = DCRUNclass('all',self.sen,start=self.startat,firstorsecondset=8)
        #print("Run Code C")

    def plotImpedance(self):
        #from impedance_plot import impedance_plot
        from DCRUNclass import DCRUNclass
        dd = DCRUNclass('impedance',self.sen,start=self.startat)
        
    def instruction(self, button_command,w1):
        """run any static computations here
        """
        if button_command == 1:
            self.Set_Sens(w1)
            self.compute_A()
        if button_command == 2:
            self.Set_Sens(w1)
            self.compute_B()
        if button_command == 3:
            self.Set_Sens(w1)
            self.compute_C()
        if button_command == 4:
            self.Set_Sens(w1)
            self.compute_D()
        if button_command == 5:
            self.Set_Sens(w1)
            self.plotImpedance()
        if button_command == 6:
            self.Set_Sens(w1)
            self.compute_E()

if __name__ == "__main__":
    project = Project("Calculate DC Component")
    project.window()


