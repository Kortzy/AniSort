import sys
import os
import PyQt5.QtWidgets as qtw
import PyQt5.uic as qtu
import json
import GUITests.Functions as func
import time
import threading

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
        AL = func.DicTrim(AL)
        #change window
        self.Mscreen = main_screen()
        widget.addWidget(self.Mscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        #multithread merge_sort in background
        self.t = threading.Thread(target = self.wrapper, args = (AL,))
        self.t.daemon = True
        self.t.start()

    def wrapper(self, AnimeList):
        json.dump(self.Mscreen.merge_sort(AnimeList),open("Sorted_Anime_List.json","w"), indent=4)

#create class that contains the main screen
class main_screen(qtw.QDialog):

    def __init__(self):
        super(main_screen,self).__init__()
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

    #merge
    def merge(self, HalfA, HalfB):
        if len(HalfA) == 0:
            return HalfB
        if len(HalfB) == 0:
            return HalfA
        R = []
        Counter1 = Counter2 = 0
        #request the cover images of the first 2 animes
        Pixmap1 = func.CoverRequest(HalfA[Counter1]["idAnilist"])
        Pixmap2 = func.CoverRequest(HalfB[Counter2]["idAnilist"])
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
                Pixmap1 = func.CoverRequest(HalfA[Counter1]["idAnilist"])
                Pixmap2 = func.CoverRequest(HalfB[Counter2]["idAnilist"])
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