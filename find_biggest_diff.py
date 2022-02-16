"""
Gets the biggest difference between available and total seats for some 
class CSV file. Useful for figuring out which graphs to make.
"""

from os import listdir
from os.path import isfile, join
from typing import Tuple

AT_LEAST = 100
OUT_SEC_FOLDER = './section'
OUT_OVERALL_FOLDER = './overall'

def get_max_diff(folder_name: str) -> Tuple[str, int, int]:
    files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]

    file_name = ""
    diff = 1
    a = 0
    t = 0
    for file in files:
        with open(join(folder_name, file), 'r') as f:
            # get last line in file
            last_line = f.readlines()[-1]
            content = last_line.split(',')
            try:
                available = int(content[1])
                total = int(content[3])
            except:
                continue  
            
            if total < AT_LEAST:
                continue 
            
            if total == 0 or available / total >= diff:
                continue 

            diff = available / total
            file_name = file
            a = available
            t = total
    return file_name, a, t

print(f'Section: {get_max_diff(OUT_SEC_FOLDER)}')
print(f'Overall: {get_max_diff(OUT_OVERALL_FOLDER)}')
input()