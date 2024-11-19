# app/models.py

from datetime import datetime
import csv
import os

CSV_FILE = 'guess_data_results.csv'
CSV_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', CSV_FILE
)



def create_csv(csv_path = CSV_FILE_PATH):
    if not os.path.exists(csv_path):
        with open(csv_path, mode='ab') as file:  # 'ab' for appending in binary mode
            writer = csv.writer(file)
            writer.writerow(["datetime", "animal", "isGuess", "isGuessCorrect"])

def add_row_csv(animal, isGuess, isGuessCorrect, csv_path = CSV_FILE_PATH):
    try:
        now = datetime.now()

        with open(csv_path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([now.strftime('%Y-%m-%d-%H-%M-%S'), animal, isGuess, isGuessCorrect])

    except Exception as e:
        raise Exception("Error saving data: {}".format(str(e)))
