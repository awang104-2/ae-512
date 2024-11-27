import csv
import os


def write_to_csv(file_name, data, headers):
    path_name = os.path.abspath(file_name)
    with open(path_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for i in range(len(data)):
            writer.writerow(data[i])


def combine_data(*args):
    return zip(args)