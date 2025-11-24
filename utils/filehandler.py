import csv
def read_csv(filename):
    data = []
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(filename, data):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)