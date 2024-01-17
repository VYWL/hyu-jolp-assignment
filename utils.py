import csv

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            [key, value] = row[0].split('\t')
            data.append((key, value))
    return data
