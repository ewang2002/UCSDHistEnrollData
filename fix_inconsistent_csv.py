"""
Attempts to fix inconsistent times (usually times off by <10ms) and rows in
CSV file.

In the original implementation of the tracker, the timestamp used was
based on when the particular section was saved and not when all similar
sections were saved.
"""
import sys
from os.path import exists

DELTA = 10


def fix_inconsistent_csv(file_name: str, output_file_name: str, folder: str) -> None:
    lines_changed = 0
    lined_iterated = 0
    removed = 0
    with open(output_file_name, 'w') as fixed_file:
        with open(file_name, "r") as f:
            init = False
            prev_time = -1
            for l in f:
                line = l.split(',')
                # remove meeting column
                # if len(line) == 9:
                #    line.pop()
                #    line[-1] += '\n'

                # invalid csv row
                if folder == "SP22":
                    if len(line) < 8:
                        removed += 1
                        continue
                elif (len(line) < 9):
                    removed += 1
                    continue

                lined_iterated += 1
                temp_line = ','.join(line)
                if not init:
                    fixed_file.write(f'{temp_line}')
                    init = True
                    continue

                time = int(line[0])

                # Initial base case
                if prev_time == -1:
                    fixed_file.write(f'{temp_line}')
                    prev_time = time
                    continue

                # Switched to a different section
                if abs(time - prev_time) > DELTA:
                    fixed_file.write(f'{temp_line}')
                    prev_time = time
                    continue

                # Same time
                if time == prev_time:
                    fixed_file.write(f'{temp_line}')
                    continue

                # Problematic line
                line[0] = str(prev_time)
                temp_line = ','.join(line)
                fixed_file.write(f'{temp_line}')
                lines_changed += 1

    print(f'Fixed {lines_changed} lines & removed {removed} lines (out of {lined_iterated} total lines).')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: fix_inconsistent_csvs.py <file>")
        sys.exit(1)

    file_name = sys.argv[-1]
    if not exists(file_name):
        print(f"File '{file_name}' does not exist")
        sys.exit(1)

    new_file_name = sys.argv[-1].split('.')[0] + '_cleaned.csv'
