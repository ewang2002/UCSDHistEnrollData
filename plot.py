from os import listdir, mkdir
from os.path import exists, join
import sys
from typing import List
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from multiprocessing import Process
import gc

OVERALL_FOLDER = 'overall'
OVERALL_PLOT_FOLDER = 'plot_overall'
SECTION_FOLDER = 'section'
SECTION_PLOT_FOLDER = 'plot_section'
CHUNK_SIZE = 30
PROCESS_COUNT = 4


def process_overall(files: List[str], from_folder: str, out_folder: str):
    """
    Processes the folder containing overall data.
    :param path: The path to the overall folder.
    """
    for file in files:
        print(f"\tProcessing {file}.")

        # Read in our CSV file
        df = pd.read_csv(join(from_folder, file))

        # Adjust the figure so it's big enough for display
        plt.figure(figsize=(15, 7))

        # Plot the number of available & waitlisted seats
        plot = sns.lineplot(data=df, x='time', y='available', color='red', label='Available')
        sns.lineplot(data=df, x='time', y='waitlisted', color='blue', label='Waitlist')

        # Modify plot properties to make it more readable
        plot.set_title(file.replace('.csv', ''))
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
        plot.xaxis.set_major_locator(ticker.MultipleLocator(60))

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
    if dt not in ['s', 'o']:
        print(f"Invalid data type '{dt}' - must be 's' (section) or 'o' (overall)")
        sys.exit(1)

    plot_folder = join(base_folder, OVERALL_PLOT_FOLDER if dt == 'o' else SECTION_PLOT_FOLDER)
    if not exists(plot_folder):
        mkdir(plot_folder)

    in_folder = join(base_folder, OVERALL_FOLDER if dt == 'o' else SECTION_FOLDER)
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
            p = Process(target=process_overall, args=(chunks[completed + i], in_folder, plot_folder))
            p.start()
            processes.append(p)
        
        # Wait for all processes to finish
        for p in processes:
            p.join()
            completed += 1