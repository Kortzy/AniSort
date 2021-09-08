import sys
import os
import requests
import PyQt5.QtWidgets as qtw
import PyQt5.uic as qtu
import PyQt5.QtGui as qtg
import json



def DicTrim(Anime_List):
    Anime_List = [{**{k:v for k,v in d.items() if k not in ["synonyms","format","idMal","private","notes","status"]},**{"Wins":0,"Losses":0}} for d in Anime_List if d["status"] == "COMPLETED"]

class browse(qtw.QDialog):
    def __init__(self):
        super(browse,self).__init__()
        qtu.loadUi("Browse.ui",self)
        self.browse.clicked.connect(self.browsefile)
        self.start.clicked.connect(self.startsort)


    def browsefile(self):
        FileName = qtw.QFileDialog.getOpenFileName(self, "Open file", os.getcwd(),"json files (*.json)")
        self.JsonFile.setText(FileName[0])
    
    def startsort(self):
        AL = json.load(open(self.JsonFile.text()))
        DicTrim(AL)
        widget.addWidget(main_screen())
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(920)
        widget.setFixedHeight(652)

class main_screen(qtw.QDialog):
    def __init__(self):
        super(main_screen,self).__init__()
        qtu.loadUi("MainScreen.ui",self)


app=qtw.QApplication(sys.argv)
widget = qtw.QStackedWidget()
widget.addWidget(browse())
widget.setFixedWidth(530)
widget.setFixedHeight(240)
widget.show()
sys.exit(app.exec_())