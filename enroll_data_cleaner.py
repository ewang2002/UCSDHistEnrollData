"""
Attempts to sort the given enrollment.csv file so that each course is in its
own file. Sorting is done in two different ways:
- One where all seat counts are merged across all sections of a course and
  put into its own file (timestamped, of course).
- Another where all seat counts are sorted based on sections (e.g. for some 
  course with two sections AXX and BXX, seat counts are separated).
These are put into the `overall` and `sec` folders, respectively. 
"""

from datetime import datetime


OUT_SEC_FOLDER = './section'
OUT_OVERALL_FOLDER = './overall'

# Key = subject + course code (e.g. CSE 100)
# Value = Dictionary where key = section code (e.g. A01 or 001)
#         and value = Dictionary where key = time
#                               and value = [available, waitlisted, total]
data_by_sec = {}

# Key = subject + course code (e.g. CSE 100)
# Value = Dictionary where key = time
#         and value = [available, waitlisted, total]
data_by_overall = {}

with open("enrollment.csv", "r") as f:
    next(f)
    for line in f:
        line = line.split(',')
        time = line[0]
        subj_course = line[1]
        section_code = line[2]
        available_seats = int(line[5])
        waitlisted = int(line[6])
        total = int(line[7])

        if subj_course not in data_by_sec:
            data_by_sec[subj_course] = {}

        if subj_course not in data_by_overall:
            data_by_overall[subj_course] = {}

        sec_code_first = section_code if section_code.isdigit() \
            else section_code[0]
        if sec_code_first not in data_by_sec[subj_course]:
            data_by_sec[subj_course][sec_code_first] = {}

        if time not in data_by_sec[subj_course][sec_code_first]:
            data_by_sec[subj_course][sec_code_first][time] = [0, 0, 0]

        if time not in data_by_overall[subj_course]:
            data_by_overall[subj_course][time] = [0, 0, 0]

        data_by_sec[subj_course][sec_code_first][time][0] += available_seats
        data_by_sec[subj_course][sec_code_first][time][1] += waitlisted
        data_by_sec[subj_course][sec_code_first][time][2] += total

        data_by_overall[subj_course][time][0] += available_seats
        data_by_overall[subj_course][time][1] += waitlisted
        data_by_overall[subj_course][time][2] += total

# save overall data into the appropriate folder
for subj_code in data_by_overall:
    with open(f'{OUT_OVERALL_FOLDER}/{subj_code}.csv', 'w') as f:
        f.write('time,available,waitlisted,total,normalized\n')
        for raw_time in data_by_overall[subj_code]:
            time = datetime.fromtimestamp(float(raw_time) / 1000.0) \
                .isoformat().split('.')[0]
            available = data_by_overall[subj_code][raw_time][0]
            waitlisted = data_by_overall[subj_code][raw_time][1]
            total = data_by_overall[subj_code][raw_time][2]
            normalized = -1 if total == 0 else available / total 
            f.write(time + ',' + str(data_by_overall[subj_code][raw_time][0]) +
                    ',' + str(data_by_overall[subj_code][raw_time][1]) + ',' +
                    str(data_by_overall[subj_code][raw_time][2]) +
                    ',' + str(normalized) + '\n')

# save section data into the appropriate folder
for subj_code in data_by_sec:
    for sec_code in data_by_sec[subj_code]:
        with open(f'{OUT_SEC_FOLDER}/{subj_code}_{sec_code}.csv', 'w') as f:
            f.write('time,available,waitlisted,total,normalized\n')
            for raw_time in data_by_sec[subj_code][sec_code]:
                time = datetime.fromtimestamp(float(raw_time) / 1000.0) \
                    .isoformat().split('.')[0]
                available = data_by_sec[subj_code][sec_code][raw_time][0]
                waitlisted = data_by_sec[subj_code][sec_code][raw_time][1]
                total = data_by_sec[subj_code][sec_code][raw_time][2]
                normalized = -1 if total == 0 else available / total 
                f.write(time + ',' + str(data_by_sec[subj_code][sec_code][raw_time][0]) +
                        ',' + str(data_by_sec[subj_code][sec_code][raw_time][1]) + ',' +
                        str(data_by_sec[subj_code]
                            [sec_code][raw_time][2]) + ','
                        + str(normalized) + '\n')
