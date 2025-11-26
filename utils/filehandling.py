import csv
def read_csv(filename):
    data = []
    with open(filename , newline="" , mode = "r") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(filename, data):
    with open(filename , newline="", mode="w") as file:
        writer = csv.writer(file)
        writer.writerows(data)