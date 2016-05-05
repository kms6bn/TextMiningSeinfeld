"""API harvester for IMDb values for Seinfeld

Example query: http://www.omdbapi.com/?t=Friends&Season=1
"""

import pandas as pd
import urllib
import json

DEFAULT_ENCODING = 'UTF-8'
OMDB_API_ENDPOINT = 'http://www.omdbapi.com/?t=Friends&Season={}'

#create empty data frame
df = pd.DataFrame()

for i in range(1, 11):
    page = urllib.request.urlopen(OMDB_API_ENDPOINT.format(i))
    text = page.read().decode('utf-8')
    for episode in json.loads(text)['Episodes']:
        rowValue = pd.Series([i] + list(episode.values()))
        df = df.append(rowValue, ignore_index=True)
        
#append missing value
episode1 = pd.Series([1, "The One with the Sonogram at the End", "", "2", "1994-09-29", "8.2"])
episode2 = pd.Series([2, "The One with Five Steaks and an Eggplant", "", "5", "1995-10-19", "8.3"])
episode3 = pd.Series([7, "The One with Ross's Library Book", "", "7", "2000-11-16", "8.6"])
episode4 = pd.Series([8, "The One with Christmas in Tulsa", "", "1", "2001-09-27", "8.6"])


df = df.append(episode1, ignore_index=True)
df = df.append(episode2, ignore_index=True)
df = df.append(episode3, ignore_index=True)
df = df.append(episode4, ignore_index=True)
       
df.columns = ["Season", "Title", "imdbID", "Episode", "Released", "imdbRating"]

#make sure numeric columns are numeric
df = df.convert_objects(convert_numeric=True)

#append wikipedia data
wiki = pd.read_csv("friendsWiki.csv")
df2 = df.merge(wiki, on="Title")

#print to csv
df2.to_csv("friendsData.csv", index=False)
#note - made manual changes to csv file
