from pathlib import Path
import os

from .context import package
from .context import PATH_TESTS_DIRECTORY

from package.functools import show_function
import package.wranglers as wgl


@show_function
def qc_scraper_consolidation():
    outputs = Path(PATH_TESTS_DIRECTORY + './scraper_consolidation').glob('**/*.csv')
    outputs_x = Path(PATH_TESTS_DIRECTORY + './scraper_consolidation_x').glob('**/*.csv')

    for filename, filename_x in zip(outputs, outputs_x):
        wgl.compare_lines_expected(filename, filename_x)

print('##################### QC Scraper Consolidation\n')

qc_scraper_consolidation()