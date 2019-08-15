from pathlib import Path
import pandas as pd
import re
import json
import os
import inspect

pd.options.mode.chained_assignment = None

def show_function(func):
    '''Decorator to print function call details - parameters names and effective values'''

    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments 
        func_args_str =  ', '.join('{} = {!r}'.format(*item) for item in list(func_args.items())[1:]) # Avoid the dataframe
        print(f'\n------- {func.__qualname__} ( {func_args_str} ) -------\n')
        return func(*args, **kwargs)

    return wrapper

def read_output(filename):
    line_count = 0
    with open(filename) as f:
        for line in f:
            data = json.loads(line)
            line_count += 1
        else :
            if line_count == 0:
                index_max = -1
            else:
                index_max = data["index"]
    return float(line_count), int(index_max)

def agg_groupby_search(x, type):
        names = {
            f'search_{type}_count': x[f'search_{type}'].count(),
            'length_sum':  x['length'].sum(),
            'length_mean': x['length'].mean(),
            'length_std':  x['length'].std()
            }
        return pd.Series(names, index=[f'search_{type}_count', 'length_sum', 'length_mean', 'length_std'])

def consolidate_outputs():
    '''Returns complete information as a dataframe on scraped file level'''

    keys = ["search_topic", "search_date", "search_location", "length", "index_max"]
    df = pd.DataFrame(columns = keys)

    for filename in Path(os.path.dirname(os.path.realpath(__file__)) + '/../data/scraper').glob('**/*.json'):
        line_count, index_max = read_output(filename)
        filename = str(filename).split("\\")[-1]
        features = re.split('_|\.[a-z]',filename)[:-1] + [line_count, index_max]
        template = dict((key, feature) for key, feature in zip(keys, features))
        df = df.append(template, ignore_index=True)

    return df

@show_function
def qc_scarping_unit(df):
    '''QC Each scraped files for indexes compared to lines'''

    expected_gap = 1

    df["gap"] = df["index_max"] - df["length"] + expected_gap
    
    df = df[df["gap"] > 0]
    df["error"] = df["gap"] / df["length"] * 100

    return df

@show_function
def qc_scraping_batches(df, batch, expected_files):
    '''QC Coherence of numbers of scraped files in a batch (location or topic)'''

    l = ['location', 'topic']
    l.remove(batch)
    elements = l[0]

    qc = df.groupby(f'search_{batch}').apply(lambda x: agg_groupby_search(x, elements)).reset_index()

    return qc[qc[f'search_{elements}_count'] != expected_files]

dataframe = consolidate_outputs()

print(qc_scarping_unit(dataframe))
print(qc_scraping_batches(dataframe, 'location', 18))
print(qc_scraping_batches(dataframe, 'topic', 12))

    