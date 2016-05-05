"""API harvester for IMDb values for Seinfeld

Example query: http://www.omdbapi.com/?t=Seinfeld&Season=1
"""

import pandas as pd
import urllib
import json

DEFAULT_ENCODING = 'UTF-8'
OMDB_API_ENDPOINT = 'http://www.omdbapi.com/?t=Seinfeld&Season={}'

#create empty data frame
df = pd.DataFrame()

#add missing episodes
episode0 = pd.Series([1, "1990-07-05", "tt0098904", "1", "7.9", "The Seinfeld Chronicles"])
df = df.append(episode0, ignore_index=True)

for i in range(1, 10):
    page = urllib.request.urlopen(OMDB_API_ENDPOINT.format(i))
    text = page.read().decode('utf-8')
    for episode in json.loads(text)['Episodes']:
        rowValue = pd.Series([i] + list(episode.values()))
        df = df.append(rowValue, ignore_index=True)
       
df.columns = ["Season", "Released", "imdbID", "Episode", "imdbRating", "Title"]

#make sure numeric columns are numeric
df = df.convert_objects(convert_numeric=True)

#update episode number for season 1
df.ix[0, 'Episode'] = 0
df.ix[1, 'Episode'] = 1
df.ix[2, 'Episode'] = 2
df.ix[3, 'Episode'] = 3
df.ix[4, 'Episode'] = 4

#append wikipedia data
wiki = pd.read_csv('seinfeldWiki.csv')
wiki['U.S. viewers\n(millions) '] = wiki['U.S. viewers\n(millions) '].str[:-4]
wiki['U.S. viewers\n(millions) '] = wiki['U.S. viewers\n(millions) '].replace({r'\[': ''}, regex=True)
df2 = df.merge(wiki, on="Title")
df3 = df.merge(df2, on="Released", how="left")

#print to csv
df3.to_csv("seinfeldData.csv", index=False)
#note - made manual changes to csv file
