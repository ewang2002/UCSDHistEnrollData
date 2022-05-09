import pandas as pd

# Get term and course from command line
term = input("Enter term: ").upper()
course = input("Enter course: ").upper()
section = input("Enter section: ").upper()

# Open the corresponding CSV file
filename = f"{term}/overall/{course}.csv" if len(section) == 0 else f"{term}/section/{course}_{section}.csv"

# Load the CSV file into a dataframe
df = pd.read_csv(filename)

prev_available = 0
prev_waitlist = 0
max_total = 0

# Iterate over each row in the dataframe
num_off = 0
for index, row in df.iterrows():
    if prev_available == 0 and prev_waitlist == 0:
        prev_available = row["available"]
        prev_waitlist = row["waitlisted"]
        continue

    # Get 'available', 'waitlisted', 'total'
    time = row["time"]
    available = int(row['available'])
    waitlisted = int(row['waitlisted'])
    total = int(row['total'])

    if total > max_total:
        max_total = total

    if available < prev_available and waitlisted < prev_waitlist:
        num_off += prev_available - available
        print(f"[{time}]: {prev_available - available} student(s) got off the waitlist.")

    prev_available = available
    prev_waitlist = waitlisted

print(f"In total, {num_off} student(s) out of {max_total} students got off the waitlist ({round((num_off / max_total) * 100, 2)}%).")