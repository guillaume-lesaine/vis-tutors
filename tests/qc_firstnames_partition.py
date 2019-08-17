from pathlib import Path
import os
import sys
sys.path.append('..')

from package.functools import *
import package.wranglers as wgl

@show_function
def qc_firstnames_temporary():
    filename = Path(os.path.dirname(os.path.realpath(__file__)) + './firstnames/firstnames_temporary.csv')
    filename_x = Path(os.path.dirname(os.path.realpath(__file__)) + './firstnames/firstnames_temporary_x.csv')

    wgl.compare_lines_expected(filename, filename_x)
    
@show_function
def qc_firstnames_partition():
    outputs = Path(os.path.dirname(os.path.realpath(__file__)) + './firstnames_partition/').glob('*.csv')
    outputs_x = Path(os.path.dirname(os.path.realpath(__file__)) + './firstnames_partition_x/').glob('*.csv')

    for filename, filename_x in zip(outputs, outputs_x):
        wgl.compare_lines_expected(filename, filename_x)

print('##################### QC Firstnames Partition\n')

qc_firstnames_temporary()
qc_firstnames_partition()