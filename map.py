import tkinter as tk
import os
class mapclass():
    def __init__(self, master):
        self.parent=master
    def drawwin(self,data):
        width=800
        height=800
        self.wnd = tk.Toplevel(master=self.parent)
        self.wnd.title("word map")
        self.wnd.geometry(f"{width}x{height}+500+0")
        canvas = tk.Canvas(self.wnd, width=width, height=height)
        for i,s in enumerate(data):
            fig = int(data[i][len(data[i]) - 2])
            canvas.create_text(30*i+30,30,text=data[i][0:len(data[i])-2])
        canvas.place(x=0, y=0)

        scroll_x = tk.Scrollbar(self.wnd, orient="horizontal", command=canvas.xview)
        scroll_x.pack(side=tk.BOTTOM,fill=tk.X)
        scroll_y = tk.Scrollbar(self.wnd, orient="vertical", command=canvas.yview)
        scroll_y.pack(side=tk.RIGHT,fill=tk.Y)
        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        canvas.configure(scrollregion=(0,0,1000,1000))
    def map(self):
        with open(os.getcwd() + "\\data\\count.txt", "r") as f:
                data = f.readlines()
        self.drawwin(data)