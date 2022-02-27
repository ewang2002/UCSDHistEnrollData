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
PLOT_FOLDER = 'plot'
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
    if len(sys.argv) != 2:
        print("Usage: plot.py <base folder>")
        sys.exit(1)

    # Get the cleaned folder
    base_folder = sys.argv[-1]
    if not exists(base_folder):
        print(f"Folder '{base_folder}' does not exist")
        sys.exit(1)

    plot_folder = join(base_folder, PLOT_FOLDER)
    if not exists(join(base_folder, PLOT_FOLDER)):
        mkdir(plot_folder)

    in_folder = join(base_folder, OVERALL_FOLDER)
    all_files = listdir(in_folder)

    # Break all_files into chunks of 10
    chunks = [all_files[i:i + CHUNK_SIZE] for i in range(0, len(all_files), CHUNK_SIZE)]

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