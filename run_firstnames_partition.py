import os
from pathlib import Path
import shutil
import re
import codecs
import unidecode
import argparse

import package.wranglers as wgl

parser = argparse.ArgumentParser()
parser.add_argument('-m', type=str, default='data', help='Mode to run the script on')
args = parser.parse_args()

path_data_directory = f'./{args.m}'
path_directory_firstnames = path_data_directory + "/firstnames"
path_directory_partition = path_data_directory + "/firstnames_partition"
path_file_temporary = path_directory_firstnames + '/firstnames_temporary.csv'

wgl.checkout_directory(path_directory_partition)
wgl.checkout_file(path_file_temporary)

def find_sex(dictionary):
    number_men, number_women = dictionary['1'], dictionary['2'] 
    sum_sex = number_men + number_women
    ratio_men, ratio_women = number_men / sum_sex, number_women / sum_sex
    
    if ratio_men >= 0.90:
        sex = 'm'
    elif ratio_women >= 0.90:
        sex = 'w'
    else:
        sex = 'u'
    
    return sex, number_men, number_women, ratio_men, ratio_women

with codecs.open(path_file_temporary, 'a', encoding="utf-8") as output:
    with codecs.open(path_directory_firstnames + '/firstnames.csv', encoding="utf-8") as firstnames:
        headers = wgl.parse_line(firstnames.readline(), r',')
        output.write('firstname,sex,number_men,number_women,ratio_men,ratio_women\n')

        w_sex, w_firstname, w_year, w_number = wgl.parse_line(firstnames.readline(), r',')
        dictionary_sex = {'1': 0, '2': 0}
        dictionary_sex[w_sex] += int(w_number)

        for line in firstnames:
            sex, firstname, year, number = wgl.parse_line(line, r',')
            if firstname == w_firstname:
                dictionary_sex[sex] += int(number)
            else :
                w_sex, number_men, number_women, ratio_men, ratio_women = find_sex(dictionary_sex)
                output.write(f'{w_firstname},{w_sex},{number_men},{number_women},{ratio_men},{ratio_women}\n')

                w_sex, w_firstname, w_year, w_number = sex, firstname, year, number
                dictionary_sex = {'1': 0, '2': 0}
                dictionary_sex[w_sex] += int(w_number)

        w_sex, number_men, number_women, ratio_men, ratio_women = find_sex(dictionary_sex)
        output.write(f'{w_firstname},{w_sex},{number_men},{number_women},{ratio_men},{ratio_women}\n')


with codecs.open(path_file_temporary, encoding="utf-8") as temp_firstnames:
    headers = wgl.parse_line(temp_firstnames.readline(), r',')

    w_firstname, w_sex, _, _, _, _ = wgl.parse_line(temp_firstnames.readline(), r',')
    w_firstname = wgl.treat_firstname(w_firstname)
    w_letter = unidecode.unidecode(w_firstname[0])
    w_file = codecs.open(path_directory_partition + f'/{w_letter}_firstnames.csv', 'a', encoding="utf-8")
    w_file.write('firstname,sex\n')
    w_file.write(f'{w_firstname},{w_sex}\n')

    for line in temp_firstnames:
        firstname, sex, _, _, _, _ = wgl.parse_line(line, r',')
        letter = unidecode.unidecode(firstname[0])

        if letter == w_letter:
            w_file.write(f'{firstname},{sex}\n')

        else:
            w_file.close()

            w_firstname, w_sex = firstname, sex
            w_letter = unidecode.unidecode(w_firstname[0])
            w_file = codecs.open(path_directory_partition + f'/{w_letter}_firstnames.csv', 'a', encoding="utf-8")
            w_file.write('firstname,sex\n')
            w_file.write(f'{w_firstname},{w_sex}\n')

    w_file.close()