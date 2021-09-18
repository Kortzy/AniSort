import sys
import os
import csv
import requests
import json
import time
import threading
import PyQt5.QtWidgets as qtw
import PyQt5.uic as qtu
import PyQt5.QtGui as qtg


# function to request anime covers from Anilist
def cover_request(AnimeID):
    query = 'query ($id: Int) {Media (id: $id, type: ANIME) {coverImage {large}}}'
    var_query = {'id': AnimeID}

    response = requests.post("https://graphql.anilist.co", json={"query": query, "variables": var_query})
    cover_url = json.loads(response.content)["data"]["Media"]["coverImage"]["large"]
    cover = qtg.QImage()
    cover.loadFromData(requests.get(cover_url).content)
    return qtg.QPixmap(cover)


def json_to_csv(json_name, csv_name):
    json_file = json.load(open(json_name))
    csv_writer = csv.writer(open(csv_name, 'w', newline='', encoding='utf-8-sig'))
    csv_writer.writerow(json_file[0].keys())
    for entries in json_file:
        csv_writer.writerow(entries.values())


# create class that contains the Browse window
class Browse(qtw.QDialog):

    def __init__(self):
        super(Browse, self).__init__()
        qtu.loadUi(os.path.join("GUI", "Browse.ui"), self)

        # set function to buttons
        self.browse_button.clicked.connect(self.browse_file)
        self.start_button.clicked.connect(self.next_window)

    # open file Browser and copy file location in text box
    def browse_file(self):
        file_name = qtw.QFileDialog.getOpenFileName(self, "Open file", os.getcwd(), "json files (*.json)")
        self.textbox.setText(file_name[0])

    # start the sorting process
    def next_window(self):
        # open and organize animeList
        # change window
        self.screen = MainScreen()
        widget.addWidget(self.screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# create class that contains the main screen
class MainScreen(qtw.QDialog):

    def __init__(self):
        super(MainScreen, self).__init__()
        qtu.loadUi(os.path.join("GUI", "MainScreen.ui"), self)

        # load and organize JSON file
        anime_list = json.load(open(browse.textbox.text()))
        anime_list = [
            {
                **{k: v for k, v in d.items() if
                   k not in ["synonyms", "format", "idMal", "private", "notes", "status", "progress"]},
                **{"Wins": 0, "Losses": 0, "Matches": 0}
            }
            for d in anime_list if d["status"] == "COMPLETED" and d["score"] >= 6 and d["format"] in ["TV", "TV_SHORT"]
        ]
        # create x and set it to 0
        self.x = 0
        # set function to buttons
        self.left_button.clicked.connect(self.left_pushed)
        self.right_button.clicked.connect(self.right_pushed)
        # multithreading merge_sort in background
        self.t = threading.Thread(target=self.wrapper, args=(anime_list,))
        self.t.daemon = True
        self.t.start()

    # dump into JSON file merge_sort output
    def wrapper(self, anime_list):
        json.dump(self.merge_sort(anime_list), open("Sorted_Anime_List.json", "w"), indent=4)
        json_to_csv("Sorted_Anime_List.json", "Sorted_Anime_List.csv")

    # change x value to meet if conditions
    def left_pushed(self):
        self.x = 1

    def right_pushed(self):
        self.x = 2

    # merge
    def merge(self, left_half, right_half):
        if len(left_half) == 0:
            return right_half

        if len(right_half) == 0:
            return left_half

        result = []
        counters = [0, 0]
        halves = [left_half, right_half]
        labels = [self.left_label, self.right_label]
        buttons = [self.left_button, self.right_button]
        # set x to 0 so that when the while loop breaks it doesn't stay at 1 or 2
        self.x = 0

        for i in range(2):
            # request the cover images of the first 2 anime and set anime covers unto the existing labels
            labels[i].setPixmap(cover_request(halves[i][counters[i]]["idAnilist"]))
            # set buttons text to anime title
            buttons[i].setText(halves[i][counters[i]]["titleRomaji"])

        # while loop to select best anime
        while len(result) < len(halves[0]) + len(halves[1]):
            winner = self.x - 1
            loser = 2 - self.x

            if self.x != 0:
                halves[winner][counters[winner]]["Wins"] += 1
                halves[loser][counters[loser]]["Losses"] += 1

                for i in range(2):
                    halves[i][counters[i]]["Matches"] += 1

                result.append(halves[winner][counters[winner]])
                counters[winner] += 1

                for i in range(2):
                    if counters[i] == len(halves[i]):
                        result += halves[1-i][counters[1-i]:]
                        return result

                for i in range(2):
                    # request the cover images of the first 2 anime and set anime covers unto the existing labels
                    labels[i].setPixmap(cover_request(halves[i][counters[i]]["idAnilist"]))
                    # set buttons text to anime title
                    buttons[i].setText(halves[i][counters[i]]["titleRomaji"])

                # set x back to 0 to continue the loop
                self.x = 0
            # to not waste calculating power
            time.sleep(0.5)
        # return the sorted list
        return result

    def merge_sort(self, array):
        if len(array) < 2:
            return array
        MID = len(array) // 2
        return self.merge(
            self.merge_sort(array[:MID]),
            self.merge_sort(array[MID:]),
        )
    # create the app


app = qtw.QApplication(sys.argv)
widget = qtw.QStackedWidget()
browse = Browse()
widget.addWidget(browse)
widget.setFixedWidth(460)
widget.setFixedHeight(340)
widget.show()
# execute the app
sys.exit(app.exec_())
