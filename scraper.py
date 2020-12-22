# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:36:33 2020

@author: Philip
"""


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

URLdict = {
    "parodies": ["https://nhentai.net/parodies/", 10],
    "characters": ["https://nhentai.net/characters/", 10],
    "tags": ["https://nhentai.net/tags/", 100],
    "artists": ["https://nhentai.net/artists/", 10],
    "groups": ["https://nhentai.net/groups/", 10]
}
# Clear the output file and then append data
output_file_name = "data.js"

clear_file = open(output_file_name, "w")
clear_file.write("")
clear_file.close()

output_file = open(output_file_name, "a")

for k in URLdict:
    URL = URLdict[k][0]
    count_threshold = URLdict[k][1]
    hasNext = True
    tagsdict = {}
    
    while hasNext:
        print("Visiting", URL, "...")
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        
        tags = soup.find_all("a", class_="tag")
        for tag in tags:
            name = tag.find("span", class_="name").getText()
            count = int(tag.find("span", class_="count").getText().replace("K", "000"))
            if count >= count_threshold:
                tagsdict[name] = count
        
        nextLink = soup.find("a", class_="next")
        if nextLink is None:
            hasNext = False
        else:
            nextURL = urljoin(URL, nextLink.attrs["href"])
            URL = nextURL
        time.sleep(0.5)
    
    print(len(tagsdict), "tags have been collected for", k)
    
    print("Writing to file...")
    output_string = "var " + k + " = JSON.parse('" + json.dumps(tagsdict) + "');\n"
    output_file.write(output_string)

output_file.close()
print("Done!")