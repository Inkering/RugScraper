import requests
import csv
from bs4 import BeautifulSoup


def getRugPage(rug):
    item_id = rug
    page = requests.get(base_url + item_id)
    rugPage = BeautifulSoup(page.content, "html.parser")
    return rugPage


def getRugName(rugPage):

    try:
        rugPage = rugPage.find("div", {"class": "heading-area"})
        item_name = list(rugPage.children)[1]
        return item_name
    except AttributeError:
        pass


def getRugLink(rugPage):
    try:
        imagesoup = rugPage.find("img", {"id": "loupe"})
        item_url = imagesoup.get('src')
        return item_url
    except AttributeError:
        pass


# build a id index of numbers
item_id_list = []

count = 410
while (count < 411):
    item_id_list.append(str(count).zfill(5))
    count += 1

print(item_id_list)
print("\n")

base_url = "http://www.peterpap.com/rugDetail.cfm?rugID="

with open('rugs.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(('Name', 'ID', "Image Url"))
    for rug in item_id_list:
        RugPage = getRugPage(rug)
        RugName = getRugName(RugPage)
        RugLink = getRugLink(RugPage)
        try:
            writer.writerow((RugName, rug, RugLink))
            print(RugName)
            print(RugLink)
            print(rug)
            print("\n")
        except NameError:
            pass
