import bioread
import pandas as pd
import argparse
from matplotlib import MatplotlibDeprecationWarning
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import warnings
from matplotlib.backends.backend_pdf import PdfPages
import webbrowser
import os


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Process a .acq file and extract data.')
    parser.add_argument('file_path', type=str, help='The path to the .acq file')

    # Parse the command line arguments
    args = parser.parse_args()

    # Read the .acq file from the given path
    acq_file = bioread.read_file(args.file_path)
    channels_to_extract = ['EMG - EMG100C', 'C5 - Expression']
    data = {}

    for channel_name in channels_to_extract:
        channel = acq_file.named_channels[channel_name]
        data[channel_name] = channel.data

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Extract the EMG signal values
    emg_signal = df['EMG - EMG100C'].values
    sampling_frequency = 2000

    lowcut = 40.0  # Lower cutoff frequency (Hz)
    highcut = 200.0  # Upper cutoff frequency (Hz)
    order = 4  # Filter order
    filtered_emg_signal = butter_bandpass_filter(emg_signal, lowcut, highcut, sampling_frequency, order)

    df['filtered_emg_signal'] = filtered_emg_signal

    # Downsample the DataFrame by selecting every second row
    df = df.iloc[::2]
    df = df.dropna()
    df = df.reset_index(drop=True)

    # Set consecutive non-zero 'C5 - Expression' values to zero
    non_zero_indices = df.index[df['C5 - Expression'] != 0]
    index_rows_to_change = []
    for i in range(len(non_zero_indices) - 1):
        if non_zero_indices[i + 1] == non_zero_indices[i] + 1:
            index_rows_to_change.append(non_zero_indices[i])
    for index in index_rows_to_change:
        df.loc[index, 'C5 - Expression'] = 0

    # Ignore a warning related to colors and the version of the package
    warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)

    graph_array = [[21, 31, 121, 131, 221, 231],
                   ['Neutral with cue', 'Neutral with no cue', 'Predicted with cue', 'Predicted with no cue',
                    'Unpredicted with cue', 'Unpredicted with no cue']]
    with PdfPages('EMG_analysis.pdf') as pdf:
        for j in range(6):

            # Filter the indices 100 before and 200 after the lines with graph_array[0][j] in the column 'C5 - Expression'
            indices = df[df['C5 - Expression'] == graph_array[0][j]].index
            num_events = len(indices)

            filtered_indices = []
            for index in indices:
                filtered_indices.extend(range(max(0, index - 100), min(len(df), index + 1000)))

            # Copy only the relevant lines
            filtered_df = df.iloc[filtered_indices].copy()
            # Add column with line number and column with the event number
            filtered_df.reset_index(inplace=True)
            filtered_df.insert(4, 'Line Number', filtered_df.index)
            filtered_df['Event Number'] = (filtered_df['Line Number'] // 300)
            filtered_df['Line Number'] = filtered_df['Line Number'] % 300

            unique_event_numbers = filtered_df['Event Number'].unique()

            # Create a color map for differentiating lines by event number
            color_map = cm.get_cmap('tab10', len(unique_event_numbers))

            # Plot all lines on the same graph, grouped by event number
            plt.figure(figsize=(30, 10))

            for i, event_number in enumerate(unique_event_numbers):
                # Filter the DataFrame for rows with the current event number
                event_df = filtered_df[filtered_df['Event Number'] == event_number]

                # Plot the data for the current event number with a unique color
                plt.plot(event_df['Line Number'], event_df['filtered_emg_signal'], color=color_map(i),
                         label=f'Event {event_number}')

            plt.axvline(x=100, color='black', linestyle='--')
            # Set labels and title
            plt.xlabel('Line Number')
            plt.ylabel('filtered_emg_signal')
            plt.title(graph_array[1][j])
            plt.grid(True)
            plt.legend(title='Event Number')
            pdf.savefig()
            plt.close()

    pdf_path = os.path.abspath('EMG_analysis.pdf')

    # Check if the file exists and print the path
    if os.path.exists(pdf_path):
        print(f"PDF file saved at: {pdf_path}")
        # Optionally, open the PDF automatically
        webbrowser.open(pdf_path)
    else:
        print("Failed to create PDF file.")


if __name__ == "__main__":
    main()