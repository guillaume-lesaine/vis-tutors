from pathlib import Path
import os
import codecs

from package.functools import *
import package.wranglers as wgl

@show_function
def qc_lines(file, file_x):
    output = codecs.open(file, encoding='utf-8')
    output_x = codecs.open(file_x, encoding='utf-8') 

    for i, (line, line_x) in enumerate(zip(output, output_x)):
        line = wgl.parse_line(line, ',')
        line_x = wgl.parse_line(line_x, ',')

        for token, token_x in zip(line, line_x):
            if token != token_x:
                print(f'(O) line.{i} - {line}')
                print(f'(X) line.{i} - {line_x}')
                print(f'(O) {token} != (X) {token_x}')

outputs = Path(os.path.dirname(os.path.realpath(__file__)) + './scraper_consolidation').glob('**/*.csv')
outputs_x = Path(os.path.dirname(os.path.realpath(__file__)) + './scraper_consolidation_x').glob('**/*.csv')

for filename, filename_x in zip(outputs, outputs_x):
    qc_lines(filename, filename_x)