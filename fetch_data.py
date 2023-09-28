"""HTML Data Fetcher

This script fetches the html files from webpages specified by an input file, 
and saves the HTML pages to disk.

The input file is a tab-delimited csv containing the following pieces of 
information:

    url file_name.csv

where 'url' is the actual link to the HTML page and 'file_name.csv' is the name 
that should be used for creating the file on disk.

This script will examine the input for any files, and will also examine the 
directory where the HTML files will be saved. If the name of the file already 
exists in the directory, then that file's HTML page will not be fetched. This 
allows the script to only fetch HTML files not already collected in the 
specified directory.

Any html files already in the directory, but not named in the input file are 
left untouched.

If the specified save directory does not exist, a new directory will be 
created in the same directory whee this script is executed.

This script requires two arguments:
    input_file.csv
        The name of the input file having the correct format
    html_directory
        The name of the directory where all of the files should be saved
"""
import sys          # Command line arguments
import os           # Check for file and directory existence
import pathlib      # Navigate the file system
import csv          # Parse CSV files
import requests     # GET requests

if __name__ == "__main__":

    # We need to know where to get the links, and where to save the fetched 
    # HTML files, as such we need to make sure two arguments are supplied
    if len(sys.argv) != 3:
        print("Usage: python fetch_data.py" + " " + 
            "<path_to/input_file.csv> <path_to/html_save_directory>")
        sys.exit()

    # We can't collect the data without knowing where to get, and where to save 
    # it
    if not os.path.isfile(sys.argv[1]):
        print("The first argument must be an existing file")
        sys.exit()
    input_file = sys.argv[1]

    if not os.path.isdir(sys.argv[2]):
        os.makedirs(sys.argv[2])
    html_save_directory = sys.argv[2]

    # We first collect all of the links and file names from the input file
    links = []
    with open(input_file) as input:
        link_reader = csv.reader(input, delimiter = "\t")
        for row in link_reader:
            links.append((row[0], row[1]))
    
    # We can save a lot of processing power by making sure we don't fetch HTML 
    # files that were already previously fetched
    saved_html_files = []
    for path in pathlib.Path(html_save_directory).iterdir():
        saved_html_files.append(path.name)

    files_to_fetch = []
    for link in links:
        if link[1] not in saved_html_files:
            files_to_fetch.append(link)

    # Make sure to fetch any HTML files that were not previously fetched
    for file in files_to_fetch:
        result = requests.get(file[0])
        new_html_file = open(html_save_directory + "/" + file[1], "w")
        new_html_file.write(result.text)
        new_html_file.close()
