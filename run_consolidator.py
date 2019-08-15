import os
import json
import re
import pandas as pd
from pathlib import Path
import shutil

def checkout(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

directory_consolidated = "./data/consolidator/units"
directory_global = "./data/consolidator/globals"

checkout(directory_consolidated)
checkout(directory_global)

df_topics = pd.read_csv("./data/context/search_topics.csv", sep=';', index_col='search_topic')
df_locations = pd.read_csv("./data/context/search_locations.csv", sep=';', index_col='search_location')

for filename in Path('./data/scraper').glob('**/*.json'):
    filestr = str(filename).split("\\")[-1]
    filestr_parts = re.split('_|\.[a-z]',filestr)[:-1]
    search_topic, search_location = filestr_parts[0], filestr_parts[2].title()
    search_topic, search_location = df_topics.loc[search_topic, 'topic'], df_locations.loc[search_location, 'location']

    with open(directory_consolidated + f'/{search_topic}_{search_location}.csv', 'a') as output:
        with open(filename) as f:
            for i, line in enumerate(f):

                line = line.replace('"rating": null, "reviews": null', '"rating": "0", "reviews": "0 avi"')
                data = json.loads(line)
                data.pop('website')

                data["search_topic"], data["search_location"] = search_topic, search_location

                if i == 0:
                    csv_header = [str(x) for x in data.keys()]
                    csv_header = ','.join(csv_header) + '\n'
                    output.write(csv_header)
                else :
                    pass

                if data["teacher"]:
                    data["url"] = re.sub(r'(https://www.superprof.fr/|.html)', '', data["url"])
                    data["teacher"] = data["teacher"].strip()
                    data["reviews"] = data["reviews"].split(' ')[0]
                    data["price"] = data["price"].replace('€ ', '')
                    csv_body = [str(x) for x in data.values()]
                    csv_body = ','.join(csv_body) + '\n'
                    try:
                        output.write(csv_body)
                    except:
                        continue
                else :
                    pass


with open(directory_global + "/global.csv","a") as output:
    first = True
    for filename in Path(directory_consolidated).glob('*.csv'):
        with open(filename) as input:
            for i, line in enumerate(input):
                if i == 0:
                    if first:
                        output.write(line)
                        first = False
                else:
                    output.write(line)
