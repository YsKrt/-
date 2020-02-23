import os
import wikipedia as wiki
import tkinter as tk

class usewiki():
    def __init__(self):
        self.abstract=[]
        self.words=[]
    def do(self):
        self.abstract.clear()
        wiki.set_lang("ja")
        for s in self.words:
            try:
                self.searchlist = wiki.search(s)
                self.content = wiki.page(self.searchlist[0]).content
            except wiki.DisambiguationError as e:
                self.content = wiki.page(e.options[0]).content
            self.abstract.append("　"+self.content[0:self.content.find("。")+1]+"\n")
    def prepare(self):
        with open(os.getcwd() + "\\data\\keys.csv","r") as f:
            self.words=f.readlines()
    def use(self,master):
        self.prepare()
        self.do()
        self.show(master)
    def show(self,master):
        self.child = tk.Toplevel(master=master)
        self.child.title("wiki")
        self.child.geometry("500x500+0+500")
        memo = tk.Text(self.child)
        memo.pack(expand=True,fill=tk.BOTH)
        for i, s in enumerate(self.abstract):
            memo.insert(f"{float(i + 1)}", s)