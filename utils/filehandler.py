import csv
def read_csv(filename):
    data = []
    try:
        with open(filename, newline="", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data
def write_csv(filename, data, fieldnames):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)