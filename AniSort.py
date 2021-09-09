import sys
import os
import requests
import json
import time
import threading
import PyQt5.QtWidgets as qtw
import PyQt5.uic as qtu
import PyQt5.QtGui as qtg

#create class that contains the browse window
class browse(qtw.QDialog):

    def __init__(self):
        super(browse,self).__init__()
        qtu.loadUi("GUITests\Browse.ui",self)

        #set function to buttons
        self.browse.clicked.connect(self.browsefile)
        self.start.clicked.connect(self.startsort)

    #open file browser and copy file location in text box
    def browsefile(self):
        FileName = qtw.QFileDialog.getOpenFileName(self, "Open file", os.getcwd(),"json files (*.json)")
        self.JsonFile.setText(FileName[0])
    #start the sorting process
    def startsort(self):
        #open and organize animeList
        AL = json.load(open(self.JsonFile.text()))
        AL = [{**{k:v for k,v in d.items() if k not in ["synonyms","format","idMal","private","notes","status"]},**{"Wins":0,"Losses":0}} for d in AL if d["status"] == "COMPLETED"]
        #change window
        self.screen = mainscreen()
        widget.addWidget(self.screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        #multithread merge_sort in background
        self.t = threading.Thread(target = self.wrapper, args = (AL,))
        self.t.daemon = True
        self.t.start()

    def wrapper(self, AnimeList):
        json.dump(self.screen.merge_sort(AnimeList),open("Sorted_Anime_List.json","w"), indent=4)

#create class that contains the main screen
class mainscreen(qtw.QDialog):

    def __init__(self):
        super(mainscreen,self).__init__()
        qtu.loadUi("GUITests\MainScreen.ui",self)
        #create x and set it to 0
        self.x = 0
        #set function to buttons
        self.button1.clicked.connect(self.pushed1)
        self.button2.clicked.connect(self.pushed2)
    
    #change x value to meet if conditions
    def pushed1(self):
        self.x = 1

    def pushed2(self):
        self.x =2

    #function to request anime covers from Anilist
    def CoverRequest(self, AnimeID):
        query = 'query ($id: Int) {Media (id: $id, type: ANIME) {coverImage {large}}}'
        varQuery = {'id': AnimeID}

        response = requests.post("https://graphql.anilist.co", json={'query': query, 'variables': varQuery})
        Cover = json.loads(response.content)["data"]["Media"]["coverImage"]["large"]
        CoverX = qtg.QImage()
        CoverX.loadFromData(requests.get(Cover).content)
        CoverX = qtg.QPixmap(CoverX)
        return CoverX

    #merge
    def merge(self, HalfA, HalfB):
        if len(HalfA) == 0:
            return HalfB
        if len(HalfB) == 0:
            return HalfA
        R = []
        Counter1 = Counter2 = 0
        #request the cover images of the first 2 animes
        Pixmap1 = self.CoverRequest(HalfA[Counter1]["idAnilist"])
        Pixmap2 = self.CoverRequest(HalfB[Counter2]["idAnilist"])
        #set anime covers unto the existing labels
        self.label1.setPixmap(Pixmap1)
        self.label2.setPixmap(Pixmap2)
        #set buttons text to anime title
        self.button1.setText(HalfA[Counter1]["titleRomaji"])
        self.button2.setText(HalfB[Counter2]["titleRomaji"])
        #set x to 0 so that when the while loop breaks it does't stay at 1 or 2
        self.x = 0
        #while loop to select best anime
        while len(R) < len(HalfA) + len(HalfB):
            if self.x == 1:
                R.append(HalfA[Counter1])
                Counter1 += 1
            elif self.x == 2:
                R.append(HalfB[Counter2])
                Counter2 += 1
            #break when 1 of the lists ends
            if Counter2 == len(HalfB):
                R += HalfA[Counter1:]
                break
            if Counter1 == len(HalfA):
                R += HalfB[Counter2:]
                break
            if self.x != 0:
                #request new anime covers
                Pixmap1 = self.CoverRequest(HalfA[Counter1]["idAnilist"])
                Pixmap2 = self.CoverRequest(HalfB[Counter2]["idAnilist"])
                #set new anime covers unto the existing labels
                self.label1.setPixmap(Pixmap1)
                self.label2.setPixmap(Pixmap2)
                #set buttons text to new anime title
                self.button1.setText(HalfA[Counter1]["titleRomaji"])
                self.button2.setText(HalfB[Counter2]["titleRomaji"])
                self.x = 0
            #to not waste calculating power
            time.sleep(0.5)
        #return the sorted list
        return R
    def merge_sort(self, array):
        if len(array) < 2:
            return array
        MID = len(array) // 2
        return self.merge(
            self.merge_sort(array[:MID]),
            self.merge_sort(array[MID:]),
            )      
#create the app
app=qtw.QApplication(sys.argv)
widget = qtw.QStackedWidget()
widget.addWidget(browse())
widget.setFixedWidth(460)
widget.setFixedHeight(340)
widget.show()
#execute the app
sys.exit(app.exec_())
