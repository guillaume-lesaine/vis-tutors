import os
import shutil
import re
import codecs
import unidecode

def checkout_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def checkout_file(file):
    if os.path.exists(file):
        os.remove(file)

def parse_line(string, sep):
    return re.split(sep, string.strip())

def search_firstname(filename, firstname):
    with codecs.open(filename, encoding = "utf-8") as f:
        for line in f:
            firstname_candidate, sex_candidate = re.split(',', line.strip())
            if firstname == firstname_candidate:
                return firstname_candidate, sex_candidate
    return 'u'

def treat_firstname(string):
    string = string.replace('-', ' ')
    return string

def compare_lines_expected(file, file_x):
    output = codecs.open(file, encoding='utf-8')
    output_x = codecs.open(file_x, encoding='utf-8')

    message_global = f'\n[O] {file}\n[X] {file_x}\n\n'
    show_message = False

    for i, (line, line_x) in enumerate(zip(output, output_x)):
        message_local = ''
        line = re.split(',', line.strip())
        line_x = re.split(',', line_x.strip())

        for token, token_x in zip(line, line_x):
            if token != token_x:
                message_local += f'(O) {token} != (X) {token_x}\n'

        if message_local != '':
        
            message_global += f'(O) line.{i} - {line}\n(X) line.{i} - {line_x}\n' + message_local
            show_message = True

    if show_message:
        print(message_global)