# Spring 2022 Enrollment Data
Enrollment data for Spring 2022. 

## Supported Courses
I only have enrollment data for:
- Lower- and upper-division CSE courses.
- Lower- and upper-division COGS courses.
- Lower- and upper-division ECE courses.
- Lower- and upper-division MATH courses.

I plan on supporting more courses in future quarters.

## Enrollment Time Periods
Taken from [here](https://blink.ucsd.edu/instructors/courses/enrollment/start.html).

#### First Pass

| Level                       | Date                                                    |
| --------------------------- | --------------------------------------------------------|
| Priorities                  | February 12, 2022                                       |
| Seniors                     | February 12, 2022 through February 15, 2022             |
| Juniors                     | February 15, 2022 through February 16, 2022             |
| Sophomores                  | February 16, 2022 through February 17, 2022             |
| First-Year                  | February 17, 2022                                       |


#### Second Pass

| Level                       | Date                                                    |
| --------------------------- | --------------------------------------------------------|
| Priorities                  | February 21, 2022                                       |
| Seniors                     | February 21, 2022 through February 23, 2022             |
| Juniors                     | February 23, 2022 through February 24, 2022             |
| Sophomores                  | February 24, 2022 through February 25, 2022             |
| First-Year                  | February 25, 2022                                       |

## Files to Discard
The raw CSV files (and the cleaned files) include data which was obtained during non-enrollment periods; this information may not be useful for you, especially if you only want to see first- and second-pass data. If you only want the raw files for first- and second-pass (i.e. files that do not include non-enrollment time periods), omit the files that start with the following dates:
- `2022-02-18*`
- `2022-02-19*`
- `2022-02-20*`

Then, run the `run.sh` script with `SP22` as the only argument to get the new cleaned CSV files. Ideally, you would group the CSV files by first- or second-pass time. 

## Some Remarks
- There may be many CSV files with inaccurate data for the first day or two (e.g. CSE 110, CSE 8A). This is because I was testing the tracker and associated wrapper functions, which had many logic errors at the time.
- Each course is scraped once every ~8 minutes. This is currently dependent on the number of courses that I decide to scrape. My tracker waits 3 seconds between requests (although I could lower this), and there are 161 courses, so there is a delay of roughly 8.05 minutes (plus some more).
