import matplotlib.pyplot as plt
import os
import requests
from bs4 import BeautifulSoup
from matplotlib import pylab

from matplotlib.font_manager import FontProperties
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\meiryob.ttc')

class scrapingclass():
    def prepare(self):
        with open(os.getcwd() + "\\data\\count.txt", "r") as f:
            data = f.readlines()

        with open(os.getcwd() + "\\data\\keys.csv","w") as fi:
            num=len(data) if len(data)<6 else 5
            for i in range(num):
                s=data[i].rsplit(",",1)[0]
                fi.write(f"{s}\n")
    def  consequence(self):
        with open(os.getcwd() + "\\data\\keys.csv", encoding='shift_jis') as csv_file:
            with open(os.getcwd() + '\\data\\result.csv','w',encoding="utf-8") as f:

                for keys in csv_file:
                    result = requests.get('https://www.google.com/search?q={}/'.format(keys))
                    soup = BeautifulSoup(result.text, 'html.parser')
                    textlist = soup.findAll(True, {'class' : 'BNeawe s3v9rd AP7Wnd'})
                    list = soup.findAll(True, {'class' : 'BNeawe vvjwJb AP7Wnd'})

                    for i in range(3):
                        #タイトル
                        #a = str(list[i]).strip('<div class="BNeawe vvjwJb AP7Wnd">')
                        #result_title = a.strip('</')

                        keyword = keys.rstrip("\n")

                        # テキスト部切出し(要約)
                        if len(textlist)-1>i*2:
                            a = str(textlist[i * 2]).strip('<div class="BNeawe s3v9rd AP7Wnd">')
                            result_text = a.strip('</').encode("utf-8")
                            result_text=result_text.decode("utf-8")
                            f.write('{0},{1}\n'.format(keyword, result_text))
                            print(keyword,result_text)
    def doscraping(self):
        self.prepare()
        self.consequence()

    def drawgraph(self,data):
        #if not self.fig_is is None:
         #   return

        numlist=[]
        wordlist=[]
        self.fig_is=plt.figure()
        ax=self.fig_is.add_subplot(111)
        for i in range(5) if len(data)>=5 else range(len(data)):
            num = int(data[i].rsplit(",",1)[1])
            numlist.append(num)
            wordlist.append(data[i].rsplit(",",1)[0])
        ax.pie(numlist, labels=wordlist, autopct="%1.1f%%")
        plt.title("関連する単語の占める割合",fontproperties=fp)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=10.5,prop=fp)
        pylab.subplots_adjust(right=0.7)




