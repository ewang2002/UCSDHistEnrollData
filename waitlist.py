"""
Calculates the number of students that got off the waitlist for a course.

Note that this is NOT guaranteed to be accurate. You can think of this as
an estimate of the number of people that actually got off. In reality, this
will most likely represent a lower bound.
"""

from typing import Tuple
import pandas as pd

def get_off_waitlist_ct(filename: str, print_data: bool = False) -> Tuple[int, int]:
    # Load the CSV file into a dataframe
    df = pd.read_csv(filename)

    prev_enrolled = 0
    prev_waitlist = 0
    max_total = 0

    # Iterate over each row in the dataframe
    num_off = 0
    for index, row in df.iterrows():
        if prev_enrolled == 0 and prev_waitlist == 0:
            prev_enrolled = row["enrolled"]
            prev_waitlist = row["waitlisted"]
            continue

        # Get 'available', 'waitlisted', 'total'
        time = row["time"]
        enrolled = int(row['enrolled'])
        waitlisted = int(row['waitlisted'])
        total = int(row['total'])

        if total > max_total:
            max_total = total

        if enrolled > prev_enrolled and waitlisted < prev_waitlist:
            num_off += enrolled - prev_enrolled
            if print_data:
                print(f"[{time}]: {enrolled - prev_enrolled} student(s) got off the waitlist.")

        prev_enrolled = enrolled
        prev_waitlist = waitlisted

    if print_data:
        print(f"In total, {num_off} student(s) out of {max_total} students got off the waitlist ({round((num_off / max_total) * 100, 2)}%).")

    return num_off, max_total


if __name__ == '__main__':
    term = input("Enter term: ").upper()
    course = input("Enter course: ").upper()
    section = input("Enter section: ").upper()

    # Open the corresponding CSV file
    if len(section) == 0:
        print("You need a section to run this script.")
    get_off_waitlist_ct(f"{term}/individual_sections/{course}_{section}.csv", True)
