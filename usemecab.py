import MeCab as mecab
import os
import re
import matplotlib.pyplot as plt
from matplotlib import pylab
from matplotlib.font_manager import FontProperties
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\meiryob.ttc')

class umecab():
    def __init__(self,PATH):
        self.halfdata=[]
        self.data=[]
        self.PATH=PATH
        self.jiritu=""
        self.sahen=""
        self.removemoji="・／！？"
    def change(self,sahen,jiritu):
        self.sahen=sahen
        self.jiritu=jiritu
    def showmecab(self,text):
        self.halfdata=self.analyze(text)
        self.arrange()
        self.data=self.sort()
    def form(self,text):
        #その他取り除く
        text=re.sub(fr"[{self.removemoji}]","",text)
        #text=re.sub(r"[・　／]","",text)
        #タグとその中身を取り除く
        pattern = r'<.+>'
        text = re.sub(pattern, '', text)
        text=text.split()
        #ユニコードエラーを阻止
        text=str(text)
        text = text.encode('cp932', 'ignore')
        text = text.decode('cp932')
        return text
    def analyze(self,text):
        m = mecab.Tagger('-Ochasen')
        m.parse('')  # 文字列がGCされるのを防ぐ
        text=self.form(text)
        node = m.parseToNode(text)
        saveword = []
        while node:
            # 単語を取得
            word = node.surface
            # 品詞を取得
            pos = node.feature.split(",")[1]
            print('{0} , {1}'.format(word, pos))

            if (pos == "一般" or pos == "固有名詞" or pos==self.sahen or pos==self.jiritu or pos=="名詞接続"):
                saveword.append(word + "\n")
                print(self.jiritu)
            # 次の単語に進める
            node = node.next
        with open(os.getcwd() + "\\data\\words.txt", "a") as f:
            f.writelines(saveword)
        return saveword

    class frequency():
        def __init__(self):
            self.word = []
            self.num = []

    def arrange(self):
        data = self.frequency()
        with open(os.getcwd() + "\\data\\words.txt", "r") as f:
            data.word = f.readlines()
            for i, s in enumerate(data.word):
                data.num.append(1)
        with open(os.getcwd() + "\\data\\"+self.PATH, "a") as f:
            save = []
            for i, s in enumerate(data.word):
                    moji = s.rstrip() + "," + f"{data.num[i]}\n"
                    # print(moji)
                    save.append(moji)
            f.writelines(save)
        data.num.clear()
        data.word.clear()

        with open(os.getcwd() + "\\data\\"+self.PATH, "r") as f:
            s = f.readlines()
            for i in range(len(s)):
                data.word.append(s[i].rsplit(",",1)[0])
                data.num.append(int(s[i].rsplit(",",1)[1]))
        for i, s in enumerate(data.word):
            for j, s2 in enumerate(data.word):
                if s == s2 and data.num[i] != -1 and i < j:
                    data.num[i] += 1
                    data.num[j] = -1
                if j + 1 == len(data.word):
                    break
        os.remove(os.getcwd() + "\\data\\words.txt")
        with open(os.getcwd() + "\\data\\"+self.PATH, "w") as f:
            save = []
            for i, s in enumerate(data.word):
                if data.num[i] != -1:
                    moji = s.rstrip() + "," + f"{data.num[i]}\n"
                    # print(moji)
                    save.append(moji)
            f.writelines(save)

    def sort(self):
        data = []
        with open(os.getcwd() + "\\data\\"+self.PATH, "r") as f:
            data = f.readlines()

        for j, s2 in enumerate(data):
            for i, s in enumerate(data):
                fig = int(data[i].rsplit(",", 1)[1])
                if len(data) > 1 and j < i:
                    fig2 = int(data[j].rsplit(",", 1)[1])
                    if fig > fig2:
                        a = s
                        data[i] = data[j]
                        data[j] = a
                if i == len(data) - 1:
                    break
        # print(data)
        with open(os.getcwd() + "\\data\\"+self.PATH, "w") as f:
            f.writelines(data)
        return data

    def drawgraph(self, data):
        # if not self.fig_is is None:
        #   return
        self.fig_is = plt.figure()
        ax = self.fig_is.add_subplot(111)
        for i in range(10) if len(data) >= 10 else range(len(data)):
            num = int(data[i].rsplit(",", 1)[1])
            ax.bar(i, num, label=data[i].rsplit(",", 1)[0])
        plt.title("使用頻度の高い単語",fontproperties=fp)
        plt.xlabel("単語",fontproperties=fp)
        plt.ylabel("使用回数",fontproperties=fp)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=10.5,prop=fp)
        pylab.subplots_adjust(right=0.7)

    def saveconfig(self):
        if os.path.exists(".\\data\\config.txt")==False:
            with open(os.getcwd() + "\\data\\config.txt", "w") as f:
                f.write(self.removemoji)
        with open(os.getcwd() + "\\data\\config.txt", "a") as f:
            f.write(self.removemoji)
        with open(os.getcwd() + "\\data\\config.txt", "r") as f:
            self.removemoji=f.read()
    def removeword(self,name):
        text2=[]
        with open(f".\\data\\{name}.txt", "r") as f:
            text=f.readlines()
        for i in range(len(text)):
            text[i]=re.sub(fr"[{self.removemoji}]","DELETEWORD",text[i])
            if not "DELETEWORD" in text[i]:
               text2.append(text[i])
        with open(os.getcwd() + f"\\data\\{name}.txt", "w") as f:
            f.writelines(text2)

        #gensimによる単語のグループ化
        #C:\Users\monst\PycharmProjects\usemecab>pyinstaller main.py --onefile --noconsole でexe化できる。