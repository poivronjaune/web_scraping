#
# Web scraping examples to test Beautiful soup
#

# https://webscraper.io/test-sites/tables
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

def test1(url1):
    html_code_1 = urlopen(url1).read().decode("utf-8")

    start = html_code_1.find("<h1>") + len("<h1>")
    end = html_code_1.find("</h1>")

    soup = BeautifulSoup(html_code_1, 'lxml')
    headings_2 = soup.find_all("h2")
    print(headings_2)

    images = soup.find_all("img")
    print(images[1]['src'])
    print(images[1]['alt'])

    first_table = soup.find("table")
    rows = first_table.findAll("tr")[1:]
    last_names = []
    for row in rows:
        last_names.append(row.findAll("td")[2].get_text())
        
    print(last_names)

def test2(url2):
    html_code_2 = urlopen(url2).read().decode("utf-8")

    soup = BeautifulSoup(html_code_2, 'lxml')
    type_table = soup.find(class_="wikitable")
    body = type_table.find("tbody")
    rows = body.find_all("tr")[1:]

    mutable_types = []
    immutable_types = []
    for row in rows:
        data = row.find_all("td")
        if data[1].get_text() == "mutable\n":
            mutable_types.append(data[0].get_text())
        else:
            immutable_types.append(data[0].get_text())
    
    thumb_box = soup.find(class_="thumb")
    thumb_img_src = thumb_box.find("img")["src"]

    toc = soup.find(class_="toc")
    toc_text = [a.get_text() for a in toc.find_all("a")]

    
    print(f"Mutable types : {mutable_types}")
    print(f"Immmutable types : {immutable_types}")
    print(thumb_img_src)
    print(f"Table of contents : {toc_text}")


##############################################################################

url1 = "https://webscraper.io/test-sites/tables"
url2 = "https://en.wikipedia.org/wiki/Python_(programming_language)"

#html_code_1 = urlopen(url1).read().decode("utf-8")
#html_code_2 = urlopen(url2).read().decode("utf-8")

print("=====================================================")
print("Lauching test1")
test1(url1)
print("=====================================================")
print("Lauching test2")
test2(url2)
print("=====================================================")
