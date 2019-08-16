from pathlib import Path
import os
import codecs
import unidecode
import re
import sys
sys.path.append('..')

from package.functools import *
import package.wranglers as wgl

@show_function
def qc_parts_number(expected_number):
    print('/ QC Number of firstnames parts created\n')
    
    count = 0
    for filename in Path(os.path.dirname(os.path.realpath(__file__)) + '/../data/firstnames_partition').glob('*.csv'):
        count += 1

    try :
        assert count == expected_number
        print('-')

    except :
        print(f'Count == {count}, Expected == {expected_number}')

@show_function
def qc_parts_length():
    print('/ QC Number of firstnames in parts for each letter\n')

    dict_letters = {}
    total = 0
    for filename in Path(os.path.dirname(os.path.realpath(__file__)) + '/../data/firstnames_partition').glob('*.csv'):
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            f.readline()
            letter = unidecode.unidecode(f.readline()[0]) #Get first letter
            count = 1
            for line in f:
                count += 1
            dict_letters[letter] = count
            total += count

    attention_letters = dict(filter(lambda x: (x[0], x[1]) if x[1] < 10 else False, dict_letters.items()))

    try :
        assert attention_letters == {}
        print('-')
    except :
        print(attention_letters)

@show_function
def qc_firstname_sex_evaluation(firstnames):
    print('/ QC Sex evaluation for a list of firstnames\n')

    for firstname, sex in firstnames:
        letter = unidecode.unidecode(firstname[0])
        filename = Path(os.path.dirname(os.path.realpath(__file__)) + f'/../data/firstnames_partition/{letter}_firstnames.csv')
        firstname_candidate, sex_candidate = wgl.search_firstname(filename, firstname)
        try:
            assert sex == sex_candidate
            print('-')
        except:
            print(f"(E) {firstname} == (R) {firstname_candidate} --- (E) {sex} == (R) {sex_candidate}")
        
qc_parts_number(26)

qc_parts_length()

qc_firstname_sex_evaluation([
    ("CLAUDE", "u"), 
    ("GUILLAUME", "m"), 
    ("MARGAUX", "w"),
    ("MAXIME", "m"),
    ("PAUL", "m"),
    ("ÉTIENNE", "m")
])