import os
import shutil
import re
import codecs
import unidecode

def checkout_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def parse_line(string, sep):
    return re.split(sep, string.strip())

def search_firstname(filename, firstname):
    with codecs.open(filename, encoding = "utf-8") as f:
        for line in f:
            firstname_candidate, sex_candidate = re.split(',', line.strip())
            if firstname == firstname_candidate:
                return firstname_candidate, sex_candidate
    return 'u'