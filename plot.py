from datetime import datetime
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

SETTINGS = {
    'overall_plot_folder': 'plot_overall',
    'section_plot_folder': 'plot_section',

    'figure_size': (15, 7),
    'num_ticks': 50
}

WIDE_SETTINGS = {
    'overall_plot_folder': 'plot_overall_wide',
    'section_plot_folder': 'plot_section_wide',

    'figure_size': (50, 10),
    'num_ticks': 200
}

GRADE_SETTINGS = {
    'Priorities': {
        'line_style': 'dotted',
        'color': '#e06d34' 
    },
    'Seniors': {
        'line_style': 'dashed',
        'color': '#42cf1b'
    },
    'Juniors': {
        'line_style': 'dashdot',
        'color': '#11c7d1'
    },
    'Sophomores': {
        'line_style': (0, (3, 5, 1, 5, 1, 5)),
        'color': '#6a26d1'
    },
    'Freshmen': {
        'line_style': (0, (3, 1, 1, 1)),
        'color': '#e0e342'
    },
    'End': {
        'line_style': 'solid',
        'color': '#000000'
    }
}

QUARTER_SETTINGS = {
    'SP22': {
        'Priorities': {
            'd': ['2022-02-12', '2022-02-21'],
            't': 8
        },
        'Seniors': {
            'd': ['2022-02-12', '2022-02-21'],
            't': 12
        },
        'Juniors': {
            'd': ['2022-02-15', '2022-02-23'],
            't': 8
        },
        'Sophomores': {
            'd': ['2022-02-16', '2022-02-24'],
            't': 8
        },
        'Freshmen': {
            'd': ['2022-02-17', '2022-02-25'],
            't': 8
        },
        'End': {
            'd': ['2022-02-18', '2022-02-26'],
            't': 22
        }
    }
}

OVERALL_FOLDER = 'overall'
SECTION_FOLDER = 'section'

# Multiprocessing options
CHUNK_SIZE = 30
PROCESS_COUNT = 4


def process_overall(files: List[str], from_folder: str, out_folder: str, settings, term: str):
    """
    Processes the folder containing overall data.
    :param path: The path to the overall folder.
    """
    for file in files:
        print(f"\tProcessing {file}.")

        # Read in our CSV file
        df = pd.read_csv(join(from_folder, file))

        # Adjust the figure so it's big enough for display
        plt.figure(figsize=settings['figure_size'])

        # Plot the number of available & waitlisted seats
        plot = sns.lineplot(data=df, x='time', y='available', color='red', label='Available')
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
        plt.ylim(ymin=0)

        # To make the x-axis more readable, purposely hide some dates and then
        # adjust the labels appropriately
        plt.setp(plot.xaxis.get_majorticklabels(), rotation=45, ha="right")
        # We want NUM_TICKS ticks on the x-axis
        plot.xaxis.set_major_locator(ticker.MultipleLocator(max(floor(len(df) / settings['num_ticks']), 1)))

        if QUARTER_SETTINGS[term]: 
            all_dates = df['time'].tolist()
            # map all dates in all_dates to a tuple of string date and datetime object
            all_dates: Tuple[str, datetime] = list(map(lambda x: (x, datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")), all_dates))

            spans = []
            spans2 = []
            for k in QUARTER_SETTINGS[term]:
                s = QUARTER_SETTINGS[term][k]
                # index [0, 1] -> 0 = first pass, 1 = second pass
                for p in range(0, 2):
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

                    if p == 0:
                        plt.axvline(x=axis_date[0][0], color=GRADE_SETTINGS[k]['color'], linestyle=GRADE_SETTINGS[k]['line_style'], label=k)
                    else:
                        plt.axvline(x=axis_date[0][0], color=GRADE_SETTINGS[k]['color'], linestyle=GRADE_SETTINGS[k]['line_style'])

            # Note that the reason why I didn't just combine the lists is because I don't want to add the "End" from first pass
            # to the graph. 

            # For first-pass stuff
            for i in range(0, len(spans) - 1):
                # fill plot between combined_spans[i] and combined_spans[i+1]
                plt.axvspan(spans[i]['start'], spans[i+1]['start'], color=spans[i]['color'], alpha=0.2, label=spans[i]['legend'])

            # For second-pass stuff
            for i in range(0, len(spans2) - 1):
                # fill plot between combined_spans[i] and combined_spans[i+1]
                plt.axvspan(spans2[i]['start'], spans2[i+1]['start'], color=spans2[i]['color'], alpha=0.2)
 
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


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: plot.py <base folder> <s | o>")
        sys.exit(1)

    # Get the cleaned folder
    base_folder = sys.argv[-2]
    if not exists(base_folder):
        print(f"Folder '{base_folder}' does not exist")
        sys.exit(1)

    # Get the type of data to process
    dt = sys.argv[-1]
    if dt not in ['s', 'o', 'sw', 'ow']:
        print(f"Invalid data type '{dt}' - must be 's' (section) or 'o' (overall) or 'sw' (sec/wide) or 'ow' (ove/wide)")
        sys.exit(1)

    settings_obj = SETTINGS if dt in ['s', 'o'] else WIDE_SETTINGS

    plot_folder = join(base_folder, settings_obj['overall_plot_folder'] if dt == 'o' or dt == 'ow' else settings_obj['section_plot_folder'])
    if not exists(plot_folder):
        mkdir(plot_folder)

    in_folder = join(base_folder, OVERALL_FOLDER if dt == 'o' or dt == 'ow' else SECTION_FOLDER)
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

    # Break all_files into chunks of CHUNK_SIZE
    chunks = [all_files[i:i + CHUNK_SIZE] for i in range(0, len(all_files), CHUNK_SIZE)]
    # Begin running
    print(f'Breaking {len(all_files)} files into {len(chunks)} chunks of {CHUNK_SIZE} files each.')
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
            p = Process(target=process_overall, args=(chunks[completed + i], in_folder, plot_folder, settings_obj, base_folder.upper()))
            p.start()
            processes.append(p)
        
        # Wait for all processes to finish
        for p in processes:
            p.join()
            completed += 1