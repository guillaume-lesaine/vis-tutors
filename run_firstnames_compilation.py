import os
from pathlib import Path
import shutil
import re
import codecs
import unidecode

import package as pkg

def treat_firstname(string):
    string = string.replace('-', ' ')
    return string

path_directory_context = "./data/context"
path_directory_parts = path_directory_context + "/firstnames_parts"
path_file_compiled = path_directory_context + '/temp_firstnames_compiled.csv'

pkg.checkout_directory(path_directory_parts)

with codecs.open(path_file_compiled, 'a', encoding="utf-8") as output:
    with codecs.open(path_directory_context + '/firstnames.txt', encoding="utf-8") as firstnames:
        headers = pkg.parse_line(firstnames.readline(), r'\t')
        output.write('firstname,sex\n')

        w_sex, w_firstname, w_year, w_number = pkg.parse_line(firstnames.readline(), r'\t')
        dictionary_sex = {'1': 0, '2': 0}
        dictionary_sex[w_sex] += int(w_number)

        for line in firstnames:
            sex, firstname, year, number = pkg.parse_line(line, r'\t')
            if firstname == w_firstname:
                dictionary_sex[sex] += int(number)
            else :
                sum_sex = dictionary_sex['1'] + dictionary_sex['2']
                ratio_men, ratio_women = dictionary_sex['1'] / sum_sex, dictionary_sex['2'] / sum_sex
                if ratio_men >= 0.70:
                    w_sex = 'm'
                elif ratio_women >= 0.70:
                    w_sex = 'w'
                else:
                    w_sex = 'u'

                output.write(f'{w_firstname},{w_sex}\n')

                w_sex, w_firstname, w_year, w_number = sex, firstname, year, number
                dictionary_sex = {'1': 0, '2': 0}
                dictionary_sex[w_sex] += int(w_number)

with codecs.open(path_file_compiled, encoding="utf-8") as firstnames_compiled:
    headers = pkg.parse_line(firstnames_compiled.readline(), r',')

    w_firstname, w_sex = pkg.parse_line(firstnames_compiled.readline(), r',')
    w_firstname = treat_firstname(firstname)
    w_letter = unidecode.unidecode(w_firstname[0])
    w_file = codecs.open(path_directory_parts + f'/{w_letter}_firstnames.csv', 'a', encoding="utf-8")
    w_file.write(f'{w_firstname},{w_sex}\n')

    for line in firstnames_compiled:
        firstname, sex = pkg.parse_line(line, r',')
        letter = unidecode.unidecode(firstname[0])

        if letter == w_letter:
            w_file.write(f'{firstname},{sex}\n')

        else:
            w_file.close()

            w_firstname, w_sex = firstname, sex
            w_letter = w_firstname[0]
            w_file = codecs.open(path_directory_parts + f'/{w_letter}_firstnames.csv', 'a', encoding="utf-8")
            w_file.write(f'{w_firstname},{w_sex}\n')

    w_file.close()

os.remove(path_file_compiled)