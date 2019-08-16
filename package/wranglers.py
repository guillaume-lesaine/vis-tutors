import os
import shutil
import re

def checkout_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def parse_line(string, sep):
    return re.split(sep, string.strip())