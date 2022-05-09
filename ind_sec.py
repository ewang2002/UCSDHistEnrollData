"""
Attempts to sort the given enrollment.csv file so that each section is in its
own file. This is different from enroll_data_cleaner.py as this only splits
each section into individual files. The enroll_data_cleaner.py does this on a 
per-course basis (i.e. all sections merged into one entry) and per section
family (e.g. all A sections merged into one entry).
"""

from datetime import datetime
from os.path import exists, join
import sys

CLEANED_FOLDER = 'cleaned'
OUT_OVERALL_FOLDER = 'individual_sections'

if len(sys.argv) != 2:
    print("Usage: enroll_data_cleaner.py <base folder>")
    sys.exit(1)

# Get the cleaned folder
base_folder = sys.argv[-1]
if not exists(base_folder):
    print(f"Folder '{base_folder}' does not exist")
    sys.exit(1)

cleaned_folder = join(base_folder, CLEANED_FOLDER)

# Key = subject + course code + section (e.g. CSE 100)
# Value = Dictionary where key = section code (e.g. A01 or 001)
#         and value = Dictionary where key = time
#                               and value = [available, waitlisted, total]
data = {}

with open(join(cleaned_folder, 'enrollment.csv'), "r") as f:
    next(f)
    for line in f:
        line = line.split(',')
        time = line[0]
        subj_course = line[1]
        section_code = line[2]
        available_seats = int(line[5])
        waitlisted = int(line[6])
        total = int(line[7])
        
        # SP22 data is kind of scuffed, so we manually calculate 
        # the total enrolled. This will NOT be accurate, but is
        # better than nothing
        if base_folder == 'SP22':
            enrolled = total - available_seats
        else:
            enrolled = int(line[8])

        if subj_course not in data:
            data[subj_course] = {}

        if section_code not in data[subj_course]:
            data[subj_course][section_code] = {}

        if time not in data[subj_course][section_code]:
            data[subj_course][section_code][time] = [0, 0, 0, 0]

        data[subj_course][section_code][time][0] += available_seats
        data[subj_course][section_code][time][1] += waitlisted
        data[subj_course][section_code][time][2] += total
        data[subj_course][section_code][time][3] += enrolled

for subj_code in data:
    for sec_code in data[subj_code]:
        with open(join(base_folder, OUT_OVERALL_FOLDER, f'{subj_code}_{sec_code}.csv'), 'w') as f:
            f.write(
            'time,enrolled,available,waitlisted,total\n')
            for raw_time in data[subj_code][sec_code]:
                time = datetime.fromtimestamp(float(raw_time) / 1000.0) \
                    .isoformat().split('.')[0]
                available = data[subj_code][sec_code][raw_time][0]
                waitlisted = data[subj_code][sec_code][raw_time][1]
                total = data[subj_code][sec_code][raw_time][2]
                enrolled = data[subj_code][sec_code][raw_time][3]
                f.write(time + ',' + str(enrolled) + ',' + str(available) +
                        ',' + str(waitlisted) + ',' + str(total) + '\n')
