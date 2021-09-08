
import requests
import PyQt5.QtGui as qtg
import json


def DicTrim(Anime_List):
    return [{**{k:v for k,v in d.items() if k not in ["synonyms","format","idMal","private","notes","status"]},**{"Wins":0,"Losses":0}} for d in Anime_List if d["status"] == "COMPLETED"]

    
# Cover Request
def CoverRequest(AnimeID):
    query = 'query ($id: Int) {Media (id: $id, type: ANIME) {coverImage {large}}}'
    varQuery = {'id': AnimeID}

    response = requests.post("https://graphql.anilist.co", json={'query': query, 'variables': varQuery})
    Cover = json.loads(response.content)["data"]["Media"]["coverImage"]["large"]
    QCover = qtg.QImage()
    QCover.loadFromData(requests.get(Cover).content)
    QCover = qtg.QPixmap(QCover)

    return QCover



#Define modified Merge Sort
