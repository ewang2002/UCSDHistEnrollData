"""
Runs through all courses in individual_sections and calculates the number of students that got off the waitlist.
"""

import os
from os.path import join
import waitlist

term = input("Enter term: ").upper()
directory = f"{term}/individual_sections"

# Get all files 
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.csv')]

with open(join(term, 'wl.csv'), 'w') as f:
    f.write("course,section,off_waitlist,total\n")
    for file in files:
        print(f"Processing {file}")
        course, section = file.replace(".csv", "").split("_")
        wl, ttl = waitlist.get_off_waitlist_ct(f"{term}/individual_sections/{file}", False)
        f.write(f"{course},{section},{wl},{ttl}\n")
