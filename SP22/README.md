# Spring 2022 Enrollment Data
Enrollment data for Spring 2022. 

## Supported Courses
I only have enrollment data for:
- Lower- and upper-division CSE courses.
- Lower- and upper-division COGS courses.
- Lower- and upper-division ECE courses.
- Lower- and upper-division MATH courses.

## Enrollment Time Periods
Taken from [here](https://blink.ucsd.edu/instructors/courses/enrollment/start.html) (note that this may be updated for the most recent quarter).

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

If you only want enrollment data for first and the first week of second pass (and not anything after that), then omit any files created after `2022-02-26`.

Then, run the `run.sh` script with `SP22` as the only argument to get the new cleaned CSV files. Ideally, you would group the CSV files by first- or second-pass time. 

## Intervals
Expect a roughly **8.5 minute interval** between requests to the same course. *This means that, after I make a request for enrollment data for course X, in roughly 8.5 minutes, I will make another request for enrollment data for the same course X.* In general, there is a 3 second delay between requests, and there are 170 courses total.

## General Notes
- There may be many CSV files with inaccurate data for the first day or two (e.g. CSE 110, CSE 8A). In particular, it will look like no one has enrolled in the course for the first few days, and then all of a sudden there is a significant drop. This is because I was testing the tracker and associated wrapper functions, which had many logic errors at the time.
- Because the cleaned `enrollment.csv` file is too big, it has been omitted. To generate this file again, run `./run.sh SP22`.
- The one major mistake I made was only collecting the number of available seats (e.g. 17/35 means 17 seats are left) instead of the number of students enrolled (e.g. 17/35 means 17 students are enrolled) for each course. Due to various factors (e.g., some sections may have more students than the limit), collecting the number of students enrolled is significantly more useful than collecting the number of available seats.
    - Note that `SP22D` and all future terms have the number of students enrolled.

## Other Remarks
- I do not have data for Feb. 27 and early Feb. 28. This was due to an issue with WebReg giving me a `shibsp::ListenerException` for the day. That being said, since these two dates are after the first week of second pass, very little should have changed during these times. 