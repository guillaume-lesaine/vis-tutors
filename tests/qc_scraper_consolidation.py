from pathlib import Path
import os
import sys
sys.path.append('..')

from package.functools import *
import package.wranglers as wgl

@show_function
def qc_scraper_consolidation():
    outputs = Path(os.path.dirname(os.path.realpath(__file__)) + './scraper_consolidation').glob('**/*.csv')
    outputs_x = Path(os.path.dirname(os.path.realpath(__file__)) + './scraper_consolidation_x').glob('**/*.csv')

    for filename, filename_x in zip(outputs, outputs_x):
        wgl.compare_lines_expected(filename, filename_x)

print('##################### QC Scraper Consolidation\n')

qc_scraper_consolidation()