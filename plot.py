from datetime import datetime, timedelta
from os import listdir, mkdir
from os.path import exists, join
import sys
from typing import List, Tuple
from matplotlib import dates
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from math import floor
from multiprocessing import Process
import gc

# Settings for input/output, basic plot stuff
GENERAL_SETTINGS = {
    'id': 'general',
    'overall_plot_folder': 'plot_overall',
    'section_plot_folder': 'plot_section',

    'figure_size': (15, 7),
    'num_ticks': 50
}

WIDE_SETTINGS = {
    'id': 'wide',
    'overall_plot_folder': 'plot_overall_wide',
    'section_plot_folder': 'plot_section_wide',

    'figure_size': (50, 10),
    'num_ticks': 200
}

FSP_SETTINGS = {
    'id': 'fsp',
    'overall_plot_folder': 'plot_overall_fsp',
    'section_plot_folder': 'plot_section_fsp',

    'figure_size': (15, 7),
    'num_ticks': 50
}

OVERALL_FOLDER = 'overall'
SECTION_FOLDER = 'section'


# Settings pertaining to how vertical line indicators should look

PRIORITIES = 'Priorities Start'
SENIORS = 'Seniors Start'
JUNIORS = 'Juniors Start'
SOPHOMORES = 'Sophomores Start'
FRESHMEN = 'Freshmen Start'
END = 'End (FP/SP)'

# For summer session
UCSD_STUDENTS = 'UCSD Students Start'
OTHERS = 'Others Start'

GRADE_SETTINGS = {
    PRIORITIES: {
        'line_style': 'dotted',
        'color': '#e06d34' 
    },
    SENIORS: {
        'line_style': 'dashed',
        'color': '#42cf1b'
    },
    JUNIORS: {
        'line_style': 'dashdot',
        'color': '#11c7d1'
    },
    SOPHOMORES: {
        'line_style': (0, (3, 5, 1, 5, 1, 5)),
        'color': '#6a26d1'
    },
    FRESHMEN: {
        'line_style': (0, (3, 1, 1, 1)),
        'color': '#e0e342'
    },
    UCSD_STUDENTS: {
        'line_style': (0, (3, 5, 1, 5, 1, 5)),
        'color': '#6a26d1'
    },
    OTHERS: {
        'line_style': (0, (3, 1, 1, 1)),
        'color': '#e0e342'
    },
    END: {
        'line_style': 'solid',
        'color': '#000000'
    }
}

QUARTER_SETTINGS = {
    'SP22': {
        PRIORITIES: {
            'd': ['2022-02-12', '2022-02-21'],
            't': 8
        },
        SENIORS: {
            'd': ['2022-02-12', '2022-02-21'],
            't': 12
        },
        JUNIORS: {
            'd': ['2022-02-15', '2022-02-23'],
            't': 8
        },
        SOPHOMORES: {
            'd': ['2022-02-16', '2022-02-24'],
            't': 8
        },
        FRESHMEN: {
            'd': ['2022-02-17', '2022-02-25'],
            't': 8
        },
        END: {
            'd': ['2022-02-18', '2022-02-26'],
            't': 22
        }
    },
    'S122': {
        UCSD_STUDENTS: {
            'd': ['2022-04-11'],
            't': 8
        },
        OTHERS: {
            'd': ['2022-04-18'],
            't': 8
        },
        END: {
            'd': ['2022-06-20'],
            't': 22
        }
    },
    'S222': {
        UCSD_STUDENTS: {
            'd': ['2022-04-11'],
            't': 8
        },
        OTHERS: {
            'd': ['2022-04-18'],
            't': 8
        },
        END: {
            'd': ['2022-07-25'],
            't': 22
        }
    }
}


# Multiprocessing options
CHUNK_SIZE = 20
WIDE_CHUNK_SIZE = 10
PROCESS_COUNT = 6


def process_overall(num: int, files: List[str], from_folder: str, out_folder: str, settings, term: str):
    """
    Processes the folder containing overall data.
    :param num: The process label number (just for identification).
    :param files: List of files to process
    :param from_folder: Folder to read from
    :param out_folder: Folder to write to
    :param settings: Settings to use
    :param term: Term to process
    """

    # Uncomment if you want to skip the images that were already generated
    temp_files = [f for f in listdir(out_folder) if exists(join(out_folder, f))]
    completed = 0
    for file in files:
        print(f"\t[{num}] Processing {file}.")
        
        if file.replace('csv', 'png') in temp_files: 
            completed += 1
            print(f"\t\t[{num}] Skipped {file} (Completed {completed}/{len(files)}).")
            continue 

        # Read in our CSV file
        df = pd.read_csv(join(from_folder, file))
        if settings['id'] == 'fsp':
            end_date_str = QUARTER_SETTINGS[term][END]['d'][1]
            # Parse this date
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
            # Filter all rows in df so that the date is earlier than the end date, noting that
            # the date in df['time'] needs to be converted first
            df = df[df['time'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S") < end_date)]

        if len(df.index) == 0:
            completed += 1
            print(f"\t\t[{num}] Skipped {file} (Completed {completed}/{len(files)}).")
            continue 

        # Adjust the figure so it's big enough for display
        plt.figure(figsize=settings['figure_size'])

        # Plot the number of available & waitlisted seats
        plot = sns.lineplot(data=df, x='time', y='enrolled', color='red', label='Enrolled')
        sns.lineplot(data=df, x='time', y='waitlisted', color='blue', label='Waitlist')

        # Modify plot properties to make it more readable
        title = file.replace('.csv', '')
        if '_' in title:
            course, section = title.split('_')
            title = f'{course} (Section {section})'

        plot.set_title(title)
        plot.set_xlabel('Time')
        plot.set_ylabel('Seats')
        plot.grid(True)
        plot.margins(0)

        # Set bottom-left corner to (0, 0)
        plt.xlim(xmin=0)

        total = max(df['total'].max(), 1)
        plt.ylim(ymin=0, ymax=1.05*total)

        # To make the x-axis more readable, purposely hide some dates and then
        # adjust the labels appropriately
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45, ha="right")
        # We want NUM_TICKS ticks on the x-axis
        plot.xaxis.set_major_locator(ticker.MultipleLocator(max(floor(len(df) / settings['num_ticks']), 1)))
        plot.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        if QUARTER_SETTINGS[term]: 
            p_max = 2 if SENIORS in QUARTER_SETTINGS[term] else 1
            all_dates = df['time'].tolist()
            # map all dates in all_dates to a tuple of string date and datetime object
            all_dates: Tuple[str, datetime] = list(map(lambda x: (x, datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")), all_dates))

            spans = []
            spans2 = []
            seen_grades = set()
            
            for k in QUARTER_SETTINGS[term]:
                s = QUARTER_SETTINGS[term][k]
                # index [0, 1] -> 0 = first pass, 1 = second pass
                for p in range(0, p_max):
                    hr = s['t']
                    date = s['d'][p]
                    # find the first date in all_dates whose date is equal to date
                    # and has the closest hour to hr
                    axis_date = list(filter(lambda x: x[1].strftime("%Y-%m-%d") == date and x[1].hour == hr, all_dates))
                    if len(axis_date) == 0:
                        continue
                    (spans if p == 0 else spans2).append({
                        'start': axis_date[0][0],
                        'color': GRADE_SETTINGS[k]['color'],
                        'legend': k,
                    })

                    plt.axvline(x=axis_date[0][0], \
                        color=GRADE_SETTINGS[k]['color'], \
                        linestyle=GRADE_SETTINGS[k]['line_style'], \
                        label=None if k in seen_grades else k)
                    seen_grades.add(k)

            # Note that the reason why I didn't just combine the lists is because I don't want to add the "End" from first pass
            # to the graph. 

            seen_shades = set()
            # For first-pass stuff
            for i in range(0, len(spans) - 1):
                # fill plot between combined_spans[i] and combined_spans[i+1]
                plt.axvspan(spans[i]['start'], \
                    spans[i+1]['start'], \
                    color=spans[i]['color'], \
                    alpha=0.2, \
                    label=None if spans[i]['legend'] in seen_shades else spans[i]['legend'])
                seen_shades.add(spans[i]['legend'])

            # For second-pass stuff
            for i in range(0, len(spans2) - 1):
                # fill plot between combined_spans[i] and combined_spans[i+1]
                plt.axvspan(spans2[i]['start'], \
                    spans2[i+1]['start'], \
                    color=spans2[i]['color'], \
                    alpha=0.2, \
                    label=None if spans2[i]['legend'] in seen_shades else spans2[i]['legend'])
                seen_shades.add(spans2[i]['legend'])
 
        plt.legend()
        # Adjusts the padding
        plt.tight_layout()

        # Then, saves the figure and closes it to save memory
        fig = plot.get_figure()
        fig.savefig(join(out_folder, file.replace('.csv', '')))
        
        # Clear the plot, close it, and clear the memory
        plot.cla()
        plt.clf()
        plt.cla()
        plt.close('all')
        del plot
        del fig
        del df
        gc.collect()
        completed += 1
        print(f"\t\t[{num}] Finished {file} (Completed {completed}/{len(files)}).")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: plot.py <base folder> <'s', 'o', 'sw', 'ow', 'sfsp', 'ofsp'>")
        sys.exit(1)

    # Get the cleaned folder
    base_folder = sys.argv[-2]
    if not exists(base_folder):
        print(f"Folder '{base_folder}' does not exist")
        sys.exit(1)

    # Get the type of data to process
    dt = sys.argv[-1]
    if dt not in ['s', 'o', 'sw', 'ow', 'sfsp', 'ofsp']:
        print(f"Invalid data type '{dt}' - must be one of:")
        print("\t's' (section)")
        print("\t'o' (overall)")
        print("\t'sw' (section, wide display)")
        print("\t'ow' (overall, wide display)")
        print("\t'sfsp' (section, first/second-pass only)")
        print("\t'ofsp' (overall, first/second-pass only)")
        sys.exit(1)

    chunk_size = CHUNK_SIZE
    if dt in ['s', 'o']:
        settings_obj = GENERAL_SETTINGS
    elif dt in ['sw', 'ow']:
        settings_obj = WIDE_SETTINGS
        chunk_size = WIDE_CHUNK_SIZE
    elif dt in ['sfsp', 'ofsp']:
        settings_obj = FSP_SETTINGS

    plot_folder = join(base_folder, settings_obj['overall_plot_folder'] if dt in ['o', 'ow', 'ofsp'] else settings_obj['section_plot_folder'])
    if not exists(plot_folder):
        mkdir(plot_folder)

    in_folder = join(base_folder, OVERALL_FOLDER if dt in ['o', 'ow', 'ofsp'] else SECTION_FOLDER)
    all_files = listdir(in_folder)

    # If we're working with sections, we only want the files that appear more than once
    if dt == 's':
        file_secs = {}
        for file in all_files:
            f_name = file.split('_')[0]
            if f_name not in file_secs:
                file_secs[f_name] = [file]
            else:
                file_secs[f_name].append(file)

        all_files = []
        for f_name in file_secs:
            if len(file_secs[f_name]) > 1:
                all_files += file_secs[f_name]

    # Break all_files into chunks of chunk_size
    chunks = [all_files[i:i + chunk_size] for i in range(0, len(all_files), chunk_size)]
    # Begin running
    print(f'Breaking {len(all_files)} files into {len(chunks)} chunks of {chunk_size} files each.')
    print(f'\tWide? {dt == "sw" or dt == "ow"}')
    print(f'\tInput Folder: {in_folder}')
    print(f'\tPlot Folder: {plot_folder}')
    print(f'\tProcesses: {PROCESS_COUNT}')

    completed = 0
    while completed < len(chunks):
        processes = []
        # Limit ourselves to PROCESS_COUNT processes, or else we might
        # end up crashing the host device with too many processes.
        for i in range(PROCESS_COUNT):
            if completed + i >= len(chunks):
                break
            print(f'Starting process {i} (completed {completed}/{len(chunks)} chunks).')
            # Create a process to process the chunk
            p = Process(target=process_overall, args=(i, \
                chunks[completed + i], \
                in_folder, \
                plot_folder, \
                settings_obj, \
                base_folder.upper()))
            p.start()
            processes.append(p)
        
        # Wait for all processes to finish
        for p in processes:
            p.join()
            completed += 1