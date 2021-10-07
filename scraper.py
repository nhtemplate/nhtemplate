# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
from time import gmtime, strftime

# Starting URLs for the tag types and the threshold
URLdict = {
    "parodies": ["https://nhentai.net/parodies/", 10],
    "characters": ["https://nhentai.net/characters/", 10],
    "tags": ["https://nhentai.net/tags/", 100],
    "artists": ["https://nhentai.net/artists/", 10],
    "groups": ["https://nhentai.net/groups/", 10]
}

# Wait time in seconds between each request to avoid making requests too quickly and frequently
wait = 0.5

# Clear the output file and then prepare it for appending data
output_file_name = "data.js"

clear_file = open(output_file_name, "w")
clear_file.write("")
clear_file.close()

output_file = open(output_file_name, "a")

# For each starting URL...
for k in URLdict:
    URL = URLdict[k][0]
    count_threshold = URLdict[k][1]
    hasNext = True
    tagsdict = {}
    
    # While the page has a next button in the pagination section...
    while hasNext:
        print("Visiting", URL, "...")
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Grab all the tags and store them in the dictionary with their count
        tags = soup.find_all("a", class_="tag")
        for tag in tags:
            name = tag.find("span", class_="name").getText()
            count = int(tag.find("span", class_="count").getText().replace("K", "000"))
            if count >= count_threshold:
                tagsdict[name] = count
        
        # Grab the next page link if it exists
        nextLink = soup.find("a", class_="next")
        if nextLink is None:
            hasNext = False
        else:
            nextURL = urljoin(URL, nextLink.attrs["href"])
            URL = nextURL
        # Wait
        time.sleep(wait)
    
    # Write the tags to the file as a JavaScript object variable
    print(len(tagsdict), "tags have been collected for", k)
    
    print("Writing to file...")
    output_string = "var " + k + " = JSON.parse('" + json.dumps(tagsdict) + "');\n"
    output_file.write(output_string)

# Grab the current GMT date time and add that as a string JavaScript variable
gmt_datetime_string = strftime("%Y-%m-%d %H:%M:%S", gmtime())
output_file.write("var lastUpdatedGMT = '"+gmt_datetime_string+"';\n")

output_file.close()
print("Done!")