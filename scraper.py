import requests
import csv
from bs4 import BeautifulSoup


# Pull in a rug based on id.
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
    # don't blow up if the html attribute isn't present for that id
    except AttributeError:
        pass


def getRugLink(rugPage):
    try:
        imagesoup = rugPage.find("img", {"id": "loupe"})
        item_url = imagesoup.get('src')
        return item_url
    # don't blow up if the html attribute isn't present for that id
    except AttributeError:
        pass


print("this program scrapes rugs")
base_url = input("Please input the location of the rugs")

# build a id index of numbersb
item_id_list = []

# this fills an array item_id_list with increasingly large numbers in
# the form: 00001, 00002,... 00200, 00201
count = 410
while (count < 411):
    item_id_list.append(str(count).zfill(5))
    count += 1

# we need to be safe when opening and writing to the csv
with open('rugs.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(('Name', 'ID', "Image Url"))
    # iterates the data calls through the list of rug id's
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
