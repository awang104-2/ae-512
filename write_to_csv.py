import csv
import os


def write_to_csv(filename, data, headers):
    path_name = os.path.abspath(filename)
    with open(path_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for i in range(len(data)):
            writer.writerow(data[i])


def sort(filename, header):
    path_name = os.path.abspath(filename)
    with open(path_name, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        sorted_rows = sorted(reader, key=lambda row: row[0])  # Sort by the first column

    filename = 'data/sorted.dat'
    path_name = os.path.abspath(filename)
    with open(path_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_rows)