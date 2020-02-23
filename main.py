import tkinter as tk
import tkinter.filedialog as fd
import datetime
import os
import usemecab,map,scraping,usegensim,wiki
import matplotlib.pyplot as plt
#import japanize_matplotlib #pip install japanize-matplotlib
from matplotlib.font_manager import FontProperties
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\meiryob.ttc')

WIDTH=900
HEIGHT=300


class Frame(tk.Frame):
    def __init__(self, master=None):
        self.winins=[]
        self.child=None
        self.child2=None
        self.fig_is=None
        self.um=None
        self.um2=None
        self.var=[]
        self.um = usemecab.umecab("count.txt")
        self.um2 = usemecab.umecab("scrcount.txt")
        tk.Frame.__init__(self, master,height=HEIGHT,width=WIDTH)
        self.master.title('note pad')
        def callback():
            dt=datetime.datetime.now()
            path = os.getcwd() + "\\data\\"
            if os.path.exists(".\\data\\temporary.txt") is False:
                with open(os.getcwd() + "\\data\\temporary.txt", "w") as f:
                    f.write("")
            with open(path+"temporary.txt","r") as f:
                text=f.readlines()
            if os.path.exists(path + dt.strftime("%Y%m%d") +".txt") is False:
                with open(path + dt.strftime("%Y%m%d") +".txt", "w") as f:
                    f.write("")
            with open(path + dt.strftime("%Y%m%d") +".txt", "a") as f:
                f.write("\n"+dt.strftime("%H:%M")+"\n")
                f.writelines(text)
                f.write("\n")
            self.close()
            self.master.destroy()
        self.master.protocol("WM_DELETE_WINDOW",callback)
        def read():
            filepath = fd.askopenfilename()
            if filepath is None:
                return
            with open(filepath, "r") as f:
                data = f.read()
                return data
        def save(data):
            filepath = fd.asksaveasfilename()
            if filepath is None:
                return
            with open(filepath, "w") as f:
                f.write(data)
        ug=usegensim.usegensim()
        gensimbutton=tk.Button(self,text="gensim",command=ug.main)
        gensimbutton.place(x=500,y=0)
        def readf():
            memo.delete("1.0","end -1c")
            memo.insert("1.0",read())
        readbutton=tk.Button(self, text="read", command=readf)
        readbutton.place(x=0, y=0)
        def savef():
            save(memo.get("1.0","end -1c"))
        savebutton = tk.Button(self, text="save", command=savef)
        savebutton.place(x=50, y=0)
        def analyzef():
            self.um.showmecab(memo.get("1.0","end -1c"))
            self.createwin(self.um.halfdata)
            self.um.drawgraph(self.um.data)
            plt.show()
        mecabbutton=tk.Button(self,text="Mecab",command=analyzef)
        mecabbutton.place(x=100,y=0)
        memo= tk.Text(self)
        memo.place(x=3,y=30,width=WIDTH-6,height=HEIGHT-33)
        memo.focus_set()
        closebutton=tk.Button(self,text="close",command=self.close)
        closebutton.place(x=WIDTH-50,y=0)
        def configf():
            self.child2 = tk.Toplevel(master=self.master)
            self.winmanage(self.child2)
            self.var.append(tk.BooleanVar())
            self.var.append(tk.BooleanVar())
            if self.var[0]==None:
                self.var[0].set(False)
                self.var[1].set(False)
            rdo1=tk.Checkbutton(self.child2,text="サ変",variable=self.var[0])
            rdo1.pack()
            rdo2 = tk.Checkbutton(self.child2, text="自立",variable=self.var[1])
            rdo2.pack()
            def click():
                if self.var[0].get() == True:
                    self.var[0].set(True)
                    self.um.change("サ変接続","")
                    self.um2.change("サ変接続","")
                elif self.var[0].get() == False:
                    self.var[0].set(False)
                    self.um.change("","")
                    self.um2.change("", "")
                if self.var[1].get()==True:
                    self.var[1].set(True)
                    self.um.change("","自立")
                    self.um2.change("","自立")
                elif self.var[1].get() == False:
                    self.var[1].set(False)
                    self.um.change("","")
                    self.um2.change("","")
                self.child2.destroy()
            btn=tk.Button(self.child2,text="OK",command=click)
            btn.pack()
        def removef():
            win = tk.Toplevel(master=self.master)
            self.winmanage(win)
            win.title("remove")
            win.geometry("+0+500")
            text = tk.Entry(master=win)
            text.pack()
            text.focus()
            def ok():
                self.um.removemoji += text.get()
                self.um2.removemoji += text.get()
                self.um.saveconfig()
                self.um2.saveconfig()
                self.um.removeword("count")
                self.um2.removeword("scrcount")
                win.destroy()
            btn=tk.Button(win,text="OK",command=ok)
            btn.pack()
        removebtn=tk.Button(self,text="remove",command=removef)
        removebtn.place(x=400,y=0)
        configbutton=tk.Button(self,text="config",command=configf)
        configbutton.place(x=250,y=0)
        scrins=scraping.scrapingclass()
        def scrf():
            text=""
            scrins.doscraping()
            with open(os.getcwd() + "\\data\\result.csv", "r", encoding="utf-8") as f:
                data = f.readlines()
            for i in range(len(data)):
                for s in data[i]:
                    text=text+s
            self.um2.showmecab(text)
            scrins.drawgraph(self.um2.data)
            plt.show()
        scrbutton=tk.Button(self,text="scr",command=scrf)
        scrbutton.place(x=180,y=0)
        wikiins=wiki.usewiki()
        def wikif():
            wikiins.use(self.master)
            #self.winmanage(wikiins.child)
        wikibutton=tk.Button(self,text="wiki",command=wikif)
        wikibutton.place(x=600,y=0)
        def showgraphf():
            scrins.drawgraph(self.um2.sort())
            self.um.drawgraph(self.um.sort())
            plt.show()
        showgraphbutton = tk.Button(self,text="graph",command=showgraphf)
        showgraphbutton.place(x=300,y=0)
        def autosave(event):
            path=os.getcwd()+"\\data\\"
            if not os.path.isdir(path):
                newdir=os.mkdir(path)
            with open(path+"temporary.txt","w") as f:
                text=memo.get("1.0","end -1c")
                f.write(text)
        memo.bind("<KeyRelease>",autosave)

    ##########ウィンドウ内のウィジェット配置は以上###########
    def close(self):
        for w in self.winins:
            w.destroy()
            w=None
            self.fig_is=None
        plt.close("all")
    def createwin(self,text):
        #if not self.child is None:
         #   return
        #print(self.child)
        self.child = tk.Toplevel(master=self.master)
        self.winmanage(self.child)
        self.child.title("usemecab")
        self.child.geometry("300x300+0+500")
        memo = tk.Text(self.child)
        memo.place(x=3, y=3, width=300-6, height=300-6)
        for i,s in enumerate(text):
            memo.insert(f"{float(i+1)}", s)
        memo.insert("end","以上の単語がリストに追加されました。")


    def winmanage(self,winins):
        self.winins.append(winins)

if __name__=="__main__":

    win = Frame()
    win.pack()
    win.mainloop()