from datetime import datetime
from genericpath import isfile
from os import listdir, remove
import sys
from os.path import exists, join
import fix_inconsistent_csv

if len(sys.argv) != 2:
    print("Usage: clean_raw_csvs.py <base folder>")
    sys.exit(1)

folder = sys.argv[-1]
if not exists(folder):
    print(f"Folder '{folder}' does not exist")
    sys.exit(1)

raw_path = join(folder, 'raw')

# Clean all raw files first
for f in listdir(raw_path):
    if not isfile(join(raw_path, f)) or f.endswith('_fixed.csv'):
        continue
    if f.endswith('.csv'):
        new_file_name = join(raw_path, f.replace('.csv', '_fixed.csv'))
        print(f'Cleaning {f}')
        fix_inconsistent_csv.fix_inconsistent_csv(join(raw_path, f), new_file_name, folder)

cleaned_path = join(folder, 'cleaned')

# List all files in folder
files = [f for f in listdir(raw_path) if isfile(join(raw_path, f)) and f.endswith('_fixed.csv')]
d = {}
for file in files:
    time = datetime.strptime(file.replace('enrollment_', '')\
        .replace('_fixed.csv', '')\
        .replace(f'_{folder}', ''), '%Y-%m-%dT%H_%M_%S')
    d[time] = file
times = sorted(list(d.keys()))

# Merge the files together
init = False
with open(join(cleaned_path, 'enrollment.csv'), 'w') as f:
    for time in times:
        file = d[time]
        with open(join(raw_path, file), 'r') as g:
            lines = g.readlines()

            if len(lines) == 0:
                continue

            if init:
                lines.pop(0)
            else:
                f.write(lines[0])
                init = True
                lines.pop(0)

            for line in lines:
                f.write(line)

# And then delete the fixed files from the raw directory
for file in files:
    print(f'Deleting {file}')
    remove(join(raw_path, file))
