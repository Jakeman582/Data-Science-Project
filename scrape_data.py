"""HTML Data Scraper

"""

import sys
import os
import pathlib
import csv
from bs4 import BeautifulSoup

if __name__ == "__main__":

    # We need to know where to get the links, and where to save the fetched 
    # HTML files, as such we need to make sure two arguments are supplied
    if len(sys.argv) != 3:
        print("Usage: python fetch_data.py" + " " + 
            "<path_to/input_file.csv> <path_to/html_save_directory>")
        sys.exit()

    # We can't collect the data without knowing where to get, and where to save 
    # it
    if not os.path.isdir(sys.argv[1]):
        print("The first argument must be an existing directory " + 
            "containing the HTML files to scrape")
        sys.exit()
    html_directory = sys.argv[1]

    # We'll need to scrape every HTML file in the input directory
    html_files = []
    for path in pathlib.Path(html_directory).iterdir():
        html_files.append(html_directory + "/" + path.name)

    songs = []

    for file in html_files:

        html_file = open(file, "r")
        soup = BeautifulSoup(html_file.read(), "html5lib")
        html_file.close()
    
        decade_table = soup.find("td", attrs = {"bgcolor": "#d6eaf8"})
        decade = decade_table.find_all("h3")

        current_year = decade_table.find_next("h3")
        current_list = decade_table.find_next("ol")

        for i in range(10):

            # Track the ranking of each song in each year's list
            rank = 1
            
            for song in current_list.find_all("li"):

                # Extract the song's year
                song_year = current_year.text[:-1]

                # Extract the part of the text containing the song's author
                song_author = song.text.rsplit("\u201c", 1)[0].split(":")[1][1:]    # \u201c is a left double quote character that the web uses instead of standard "

                # Extract the part of the text containing the song's title
                song_title = song.text.rsplit("\u201c", 1)[1].split("\u201d")[0]    # \u201d is a right double quote character

                # Make sure to save the song so they can be analyzed later
                songs.append((song_year, rank, song_author, song_title))

                # The next song has a lower rank
                rank += 1
            
            current_year = current_year.find_next("h3")
            current_list = current_list.find_next("ol")

    # If the specified save file does not exist, we should just create it
    with open(sys.argv[2], "w") as file:
        song_writer = csv.writer(file, delimiter = "\t")
        for song in songs:
            song_writer.writerow(song)
