""" Data Aggregator
"""

import sys
import os
import pathlib
import csv

if __name__ == "__main__":

    AGGREGATED_DATA_FILE = "song_rankings.csv"

    songs = []

    # Collect information from Dave's Music Database
    with open("daves_music_database.csv", "r") as file:
        song_reader = csv.reader(file, delimiter = "\t")
        for row in song_reader:
            songs.append((
                row[0], 
                row[1], 
                row[2], 
                row[3]
            ))
    
    # Collect information from the Kaggle dataset
    with open("1958_2021.csv", "r") as file:
        song_reader = csv.reader(file)

        # Skip the header row
        next(song_reader)

        for row in song_reader:
            year = row[0].split("-")[0]
            if year >= "1960":
                songs.append((
                    year, 
                    row[1], 
                    row[3], 
                    row[2]
                ))
    
    with open(AGGREGATED_DATA_FILE, "w") as file:
        song_writer = csv.writer(file, delimiter = "\t", lineterminator = "\n")
        for song in songs:
            song_writer.writerow(song)