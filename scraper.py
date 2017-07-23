import requests
import csv
import sys
import os
import shutil
from bs4 import BeautifulSoup


# Pull in a rug based on id.
def getRugPage(rug):
    item_id = rug
    page = requests.get(base_url + item_id)
    rugPage = BeautifulSoup(page.content, "html.parser")
    return rugPage


# get name based on rugPage
def getRugName(rugPage):
    try:
        rugPage = rugPage.find("div", {"class": "heading-area"})
        item_name = list(rugPage.children)[1].contents
        return item_name[0]
    # don't blow up if the html attribute isn't present for that id
    except AttributeError:
        pass


# get rug desc based on rugPage
def getRugDesc(rugPage):
    try:
        rugPage = rugPage.find("article", {"class": "article"})
        item_desc = rugPage.find("p").contents
        # we only want valid ids
        if item_desc != "None":
            return item_desc
    # don't blow up if the html attribute isn't present for that id
    except AttributeError:
        pass


# get rug image url based on rugPage
def getRugLink(rugPage):
    try:
        imagesoup = rugPage.find("img", {"id": "loupe"})
        item_url = imagesoup.get('src')
        return item_url
    # don't blow up if the html attribute isn't present for that id
    except AttributeError:
        pass


# we know which ids are valid ones based on a csv input
def importIds(csv_file):
    ids = []
    # read the data file of ids, put them all in a handy dictionary
    # zfill pads leading zeros onto numbers so that they have
    # consistent length, in this case 5 digits. e.g. 00050
    with open(csv_file, newline="") as f:
        rug_reader = csv.DictReader(f)
        for row in rug_reader:
            ids.append(row["ids"].zfill(5))
    return ids


# given a url, downloads an image and then names the
# file with the given input
# titles should be of the form name-antique-rug-id
def pullImages(name, id, url):
    image_name = name + "-antique-rug-" + id + ".jpeg"
    image_url = url
    response = requests.get(image_url, stream=True)
    with open(os.path.join("Images", image_name), "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


# we need to be safe when opening and writing to the csv
def buildcsv(base):
    base_url = base
    with open('rugs.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('ID', 'Name', "Desc", "Image Url"))
        # iterates the data calls through the list of rug id's
        for rug in importIds("ids.csv"):
            RugPage = getRugPage(rug)
            RugName = getRugName(RugPage)
            RugLink = getRugLink(RugPage)
            RugDesc = getRugDesc(RugPage)
            try:
                writer.writerow((rug, RugName, RugDesc, RugLink))
                print(rug)
                print(RugName)
                print(RugLink)
                print(RugDesc)
                print("\n")
            except NameError:
                pass

def renameImage(csv_file):
    with open(csv_file, newline="") as f:
        data_reader = csv.DictReader(f)
        for row in data_reader:
            pullImages(row["Name"].replace(" ", "-"), row["ID"], row["Image Url"])
            print(row["Name"])

# get some user input on what to do next
print("this program scrapes rugs! \n")
user_response = input("would you like to fetch metadata or rename images (m or r)? ")

if user_response == "m":
    base_url = input("Whats the base url of the website ")
    buildcsv(base_url)
elif user_response == "r":
    renameImage("rugs.csv")
