import os
import csv

def save_as_csv(file_name, object):
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Name', 'Owner', 'Description', 'Homepage', 'License', 'Forks', 'Watchers', 'Date of Collection'])  # Example header
        writer.writerow(object.to_csv_row().split(','))
