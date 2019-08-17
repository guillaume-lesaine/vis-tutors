import os
import json
import re
import pandas as pd
from pathlib import Path
import codecs
import unidecode
import argparse

import package.wranglers as wgl

parser = argparse.ArgumentParser()
parser.add_argument('-m', type=str, default='data', help='Mode to run the script on')
args = parser.parse_args()

path_data_directory = f'./{args.m}'
path_directory_scraper = path_data_directory + '/scraper'
path_directory_consolidation = path_data_directory + '/scraper_consolidation'
path_directory_units = path_directory_consolidation + './units'
path_directory_globals = path_directory_consolidation + './globals'

wgl.checkout_directory(path_directory_consolidation)
wgl.checkout_directory(path_directory_units)
wgl.checkout_directory(path_directory_globals)

df_topics = pd.read_csv('./data/context/search_topics.csv', sep=';', index_col='search_topic')
df_locations = pd.read_csv('./data/context/search_locations.csv', sep=';', index_col='search_location')


for filename in Path(path_directory_scraper).glob('**/*.json'):

    filestr = str(filename).split('\\')[-1]
    filestr_parts = re.split('_|\.[a-z]',filestr)[:-1]
    search_topic, search_location = filestr_parts[0], filestr_parts[2].title()
    search_topic, search_location = df_topics.loc[search_topic, 'topic'], df_locations.loc[search_location, 'location']

    with codecs.open(path_directory_units + f'/{search_topic}_{search_location}.csv', 'a', encoding='utf-8') as output:
        with codecs.open(filename, encoding='utf-8') as input:
            output.write('index,url,search_topic,search_location,teacher,location,rating,reviews,price,first_free,ambassador,picture\n')

            for line in input:

                line = line.replace('"rating": null, "reviews": null', '"rating": "0", "reviews": "0 avi"')
                data = json.loads(line)
                data.pop('website')

                data['search_topic'], data['search_location'] = search_topic, search_location

                if data['teacher']:
                    data['url'] = re.sub(r'(https://www.superprof.fr/|.html)', '', data['url'])
                    data['teacher'] = data['teacher'].strip()
                    data['reviews'] = data['reviews'].split(' ')[0]
                    data['price'] = data['price'].replace('€ ', '')
                    line = [str(x) for x in data.values()]
                    line = ','.join(line) + '\n'
                    try:
                        output.write(line)
                    except:
                        continue
                else :
                    pass


with open(path_directory_globals + '/global.csv','a', encoding='utf-8') as output:
    first = True
    
    for filename in Path(path_directory_units).glob('*.csv'):
        with codecs.open(filename, encoding='utf-8') as input:

            headers = input.readline()
            if first:
                output.write(headers)
                first = False

            for line in input:
                output.write(line)
