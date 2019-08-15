import os
import json
import re
import pandas as pd
from pathlib import Path
import shutil



directory = "./data/scraper/consolidated"

shutil.rmtree(directory)
os.makedirs(directory)

df_topics = pd.read_csv("./data/context/search_topics.csv", sep=';', index_col='search_topic')
df_locations = pd.read_csv("./data/context/search_locations.csv", sep=';', index_col='search_location')

for filename in Path('./data/scraper').glob('**/*.json'):
    keys = ["index", "url", "search_topic", "search_location", "teacher", "location", "rating", "reviews", "price", "first_free", "ambassador", "picture"]
    df = pd.DataFrame(columns = keys)

    with open(filename) as f:
        for line in f:
            line = line.replace('"rating": null, "reviews": null', '"rating": "0", "reviews": "0 avi"')
            data = json.loads(line)
            if data["teacher"]:
                data.pop('website')
                data["url"] = re.sub(r'(https://www.superprof.fr/|.html)', '', data["url"])
                data["search_topic"] = df_topics.loc[data["search_topic"], 'topic']
                data["search_location"] = df_locations.loc[data["search_location"], 'location']
                data["teacher"] = data["teacher"].strip()
                data["reviews"] = data["reviews"].split(' ')[0]
                data["price"] = data["price"].replace('€ ', '')
                df = df.append(data, ignore_index=True)
            else :
                pass
        else :
            search_topic, search_location = data["search_topic"], data["search_location"]
            df.to_csv(directory + f'/{search_topic}_{search_location}.csv', index=False)
