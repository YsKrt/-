import gensim
from gensim import corpora
import os

class usegensim():
    def __init__(self):
        self.text=[]
    def prepare(self):
        with open(os.getcwd() + "\\data\\scrcount.txt") as f:
            self.text=f.readlines()
        for i in range(len(self.text)):
            self.text[i]=self.text[i].rsplit(",", 1)[0]
    def use(self):
        dictionary=corpora.Dictionary(self.text)
        dictionary.save_as_text(".\\data\\dic.txt")
        corpus=[dictionary.doc2bow(texts) for texts in self.text]
        lda=gensim.models.ldamodel.LdaModel(corpus=corpus,num_topics=5,id2word=dictionary)
        print(self.text)

    def main(self):
        self.prepare()
        self.use()