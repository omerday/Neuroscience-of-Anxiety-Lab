import os
import bioread
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter
from scipy.signal import filtfilt
from scipy.signal import find_peaks
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from pathlib import Path


is_event_negative = lambda x: (x>=30 and x<=40)
is_event_neutral = lambda x: (x>=50 and x<=60)
is_event_positive = lambda x: (x>=70 and x<=80)


def low_pass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data


def divide_df_to_segments(data):
    non_zero_indices = np.where(data != 0)[0]

    result = []
    for i, idx in enumerate(non_zero_indices):
        value = data[idx]
        start_index = idx
        if i < len(non_zero_indices) - 1:
            end_index = non_zero_indices[i + 1] - 1
        else:
            end_index = len(data) - 1
        if i > 0 and result[-1][0] == value:
            result[-1] = (value, result[-1][1], end_index)
        else:
            result.append((value, start_index, end_index))
    return result


def closest_time_index(time_list, new_time):
    return min(range(len(time_list)), key=lambda i: abs(time_list[i] - new_time))


def weighted_average(data):
    total_weight = sum(weight for _, weight in data)
    if total_weight == 0:
        return None  # Avoid division by zero
    return sum(value * weight for value, weight in data) / total_weight


SAMPLE_FREQ = 50
PEAK_WIDTH = SAMPLE_FREQ / 5
RESPIRATION_CHANNEL_NAME = 'DA - TSD221-MRI - Respiration Transduce'
EVENT_CHANNEL_NAME = 'C5 - Expression'


def analize_file(file_path):
    acq_file = bioread.read_file(file_path)
    respiration_channel = acq_file.named_channels[RESPIRATION_CHANNEL_NAME]
    event_channel = acq_file.named_channels[EVENT_CHANNEL_NAME]
    respiration_data = respiration_channel.data
    event_data = event_channel.data
    downsampled_data = respiration_data[::int(respiration_channel.samples_per_second/SAMPLE_FREQ)]

    filtered_data = low_pass_filter(downsampled_data, 0.7, SAMPLE_FREQ)

    # The reason for the distance and width is to deal with false positive peaks
    peaks, _ = find_peaks(filtered_data, distance=PEAK_WIDTH, width=PEAK_WIDTH)
    peak_times = peaks/SAMPLE_FREQ
    breath_intervals = np.diff(peaks) / SAMPLE_FREQ
    breathing_rate = 60 / breath_intervals

    min_interval = min(abs(peak_times[i] - peak_times[i-1]) for i in range(1, len(peak_times)))

    # This section is needed because the peak times are irregular time intervals, and so we interpolate the values over continuous time and then we can average it
    adapted_peak_times = peak_times[1:]
    uniform_times = np.linspace(min(adapted_peak_times), max(adapted_peak_times), num=int(adapted_peak_times[-1]/min_interval))
    continuous_values = np.interp(uniform_times, adapted_peak_times, breathing_rate)

    segments = divide_df_to_segments(event_data)
    # Turn from index to seconds
    ratio = event_channel.samples_per_second
    segments = [(value, start/ratio, end/ratio) for (value, start, end) in segments]

    negative_timeframes = [(start, end) for (value, start, end) in segments if is_event_negative(value)]
    neutral_timeframes = [(start, end) for (value, start, end) in segments if is_event_neutral(value)]
    positive_timeframes = [(start, end) for (value, start, end) in segments if is_event_positive(value)]

    # Find the closest time in uniform_times to each timeframe
    negative_time_indices = [(closest_time_index(uniform_times, start), closest_time_index(uniform_times, end)) for (start, end) in negative_timeframes]
    neutral_time_indices = [(closest_time_index(uniform_times, start), closest_time_index(uniform_times, end)) for (start, end) in neutral_timeframes]
    positive_time_indices = [(closest_time_index(uniform_times, start), closest_time_index(uniform_times, end)) for (start, end) in positive_timeframes]

    negative_breathing_rates = [(np.mean(continuous_values[start:end+1]), end-start) for (start, end) in negative_time_indices]
    neutral_breathing_rates = [(np.mean(continuous_values[start:end+1]), end-start) for (start, end) in neutral_time_indices]
    positive_breathing_rates = [(np.mean(continuous_values[start:end+1]), end-start) for (start, end) in positive_time_indices]

    negative_breathing_rate = weighted_average(negative_breathing_rates)
    neutral_breathing_rate = weighted_average(neutral_breathing_rates)
    positive_breathing_rate = weighted_average(positive_breathing_rates)

    return negative_breathing_rate, neutral_breathing_rate, positive_breathing_rate


def bar_plot_breathing(negative_value, neutral_value, positive_value, title, filename=None, show=False):
    plt.bar(["Negative", "Neutral", "Positive"], [negative_value, neutral_value, positive_value])
    plt.title(title)
    plt.ylabel("Breathing rate (breaths per minute)")
    if filename is not None:
        plt.savefig(filename)
    if show:
        plt.show()
    plt.clf()
    plt.close()


def main():
    input_directory = "Neuroscience-of-Anxiety-Lab/DataAnalysis/RespirationData"
    output_directory = "Neuroscience-of-Anxiety-Lab/DataAnalysis/RespirationOutput"

    negative_breathing_rates = []
    neutral_breathing_rates = []
    positive_breathing_rates = []

    for filename in os.listdir(input_directory):
        print("Analizing " + filename)
        file_path = os.path.join(input_directory, filename)
        negative_breathing_rate, neutral_breathing_rate, positive_breathing_rate = analize_file(file_path)
        negative_breathing_rates.append(negative_breathing_rate)
        neutral_breathing_rates.append(neutral_breathing_rate)
        positive_breathing_rates.append(positive_breathing_rate)
        print("VALUES")
        print(negative_breathing_rate, neutral_breathing_rate, positive_breathing_rate)
        bar_plot_breathing(negative_breathing_rate, neutral_breathing_rate, positive_breathing_rate, filename, 
            os.path.join(output_directory, Path(filename).with_suffix(".png")))
        
    bar_plot_breathing(np.mean(negative_breathing_rates), np.mean(neutral_breathing_rates), np.mean(positive_breathing_rates), 
            "Average on all files", os.path.join(output_directory, "Average.png"))



if __name__ == "__main__":
    main()

