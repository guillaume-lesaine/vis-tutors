from pathlib import Path
import os

from .context import package
from .context import PATH_TESTS_DIRECTORY

from package.functools import show_function
import package.wranglers as wgl


@show_function
def qc_firstnames_temporary():
    filename = Path(PATH_TESTS_DIRECTORY + './firstnames/firstnames_temporary.csv')
    filename_x = Path(PATH_TESTS_DIRECTORY + './firstnames/firstnames_temporary_x.csv')

    wgl.compare_lines_expected(filename, filename_x)
    
@show_function
def qc_firstnames_partition():
    outputs = Path(PATH_TESTS_DIRECTORY + './firstnames_partition/').glob('*.csv')
    outputs_x = Path(PATH_TESTS_DIRECTORY + './firstnames_partition_x/').glob('*.csv')

    for filename, filename_x in zip(outputs, outputs_x):
        wgl.compare_lines_expected(filename, filename_x)

print('##################### QC Firstnames Partition\n')

qc_firstnames_temporary()
qc_firstnames_partition()