import csv

def read_csv(filename):
    data = []
    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

def write_csv(filename, data):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)