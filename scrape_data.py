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
    #print(html_files)
    
    #---------------------------------------------------------------------------

    songs = []

    for file in html_files:

        #print("processing " + file + "...")

        html_file = open(file, "r")
        soup = BeautifulSoup(html_file.read(), "html5lib")
        html_file.close()
    
        #decade_table = soup.find('table', attrs = {"bordercolor": "blue"})
        decade_table = soup.find("td", attrs = {"bgcolor": "#d6eaf8"})
        decade = decade_table.find_all("h3")

        #print(len(decade))
        current_year = decade_table.find_next("h3")
        current_list = decade_table.find_next("ol")

        #print(current_year)
        #print(current_list)

        for i in range(10):
            #print(current_year)
            #print(current_list)
            #print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            
            for song in current_list.find_all("li"):
                #print(song.text)
                #print(current_year.text)
                # Extract the song's year
                song_year = current_year.text[:-1]
                #print(song_year)

                # Extract the part of the text containing the song's author
                song_author = song.text.rsplit("\u201c", 1)[0].split(":")[1][1:]    # \u201c is a left double quote character that the web uses instead of standard "

                # Extract the part of the text containing the song's title
                song_title = song.text.rsplit("\u201c", 1)[1].split("\u201d")[0]    # \u201d is a right double quote character

                #print(song_author + " --> " + song_title)
                # Make sure to save the song so they can be analyzed later
                songs.append((song_year, song_author, song_title))
            
            current_year = current_year.find_next("h3")
            current_list = current_list.find_next("ol")

        """ for year in decade:
            song_year = year.text[:-1]
            song_list = decade_table.find_all_next("ol")
            #print(song_list)
            print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
            for song in song_list.find_all("li"):
                # Extract the part of the text containing the song's author
                song_author = song.text.rsplit("\u201c", 1)[0].split(":")[1][1:]    # \u201c is a left double quote character that the web uses instead of standard "

                # Extract the part of the text containing the song's title
                song_title = song.text.rsplit("\u201c", 1)[1].split("\u201d")[0]    # \u201d is a right double quote character

                #songs.append((song_year, song_author, song_title)) """
                


    # If the specified save file does not exist, we should just create it
    with open(sys.argv[2], "w") as file:
        song_writer = csv.writer(file, delimiter = "\t")
        for song in songs:
            song_writer.writerow(song)
