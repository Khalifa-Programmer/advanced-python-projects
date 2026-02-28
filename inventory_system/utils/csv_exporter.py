import csv

def export_to_csv(data):
    with open("report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Quantity", "Price"])
        writer.writerows(data)
