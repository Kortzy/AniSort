import json
import os

AL = json.load(open(os.path.join(os.getcwd(),"AniList.json")))
AL = [{**{k:v for k,v in d.items() if k not in ["synonyms","format","idMal","private","notes","status"]},**{"Wins":0,"Losses":0}} for d in AL if d["status"] == "COMPLETED"]
def merge(A, B):
    if len(A) == 0:
        return B
    if len(B) == 0:
        return A
    R = []
    IA = IB = 0
    while len(R) < len(A) + len(B):
        print(A[IA]["titleRomaji"], "or", B[IB]["titleRomaji"])
        IN = input("which is the best?\nChoose with 1 or 2:")
        if IN == "1":
            print("You picked",A[IA]["titleRomaji"],":","Total Wins -",A[IA]["Wins"],"Total Losses -",A[IA]["Losses"],"Previous Score -",A[IA]["score"],"/10")
            A[IA]['Wins'] += 1
            B[IB]['Losses'] += 1
            R.append(A[IA])
            IA += 1
        elif IN == "2":
            print("You picked",B[IB]["titleRomaji"],":","Total Wins -",B[IB]["Wins"],"Total Losses -",B[IB]["Losses"],"Previous Score -  ",B[IB]["score"],"/10")
            A[IA]['Losses'] += 1
            B[IB]['Wins'] += 1
            R.append(B[IB])
            IB += 1
        else:
            print("I thought typing 1 or 2 was easy. . .")
        if IB == len(B):
            R += A[IA:]
            break
        if IA == len(A):
            R += B[IB:]
            break
    return R
def merge_sort(array):
    if len(array) < 2:
        return array
    MID = len(array) // 2
    return merge(
        A=merge_sort(array[:MID]),
        B=merge_sort(array[MID:]))
print(merge_sort(AL))
json.dump(merge_sort(AL),open("Sorted_Anime_List.json","w"))
