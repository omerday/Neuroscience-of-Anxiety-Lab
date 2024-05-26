import bioread
import pandas as pd
import argparse


def convert_acq_to_csv(acq_file_path, csv_file_path):
    # Read the .acq file from the given path
    acq_file = bioread.read_file(acq_file_path)

    # Extract the data from all channels
    data = {}
    for channel in acq_file.channels:
        channel_name = channel.name
        data[channel_name] = channel.data

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"Data successfully saved to {csv_file_path}")


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Convert a .acq file to a CSV file.')
    parser.add_argument('acq_file_path', type=str, help='The path to the .acq file')
    parser.add_argument('csv_file_path', type=str, help='The path to the output CSV file')

    # Parse the command line arguments
    args = parser.parse_args()

    # Convert the .acq file to CSV
    convert_acq_to_csv(args.acq_file_path, args.csv_file_path)


if __name__ == "__main__":
    main()