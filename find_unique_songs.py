import pandas as pd

if __name__ == "__main__":

    song_data = pd.read_csv(
        "data/song_rankings.csv", 
        delimiter = "\t", 
        names = ["year", "rank", "artist", "song"], 
        dtype = {
            "year": "Int64", 
            "rank": "Int64", 
            "artist": str, 
            "song": str
        }
    )

    song_data_deduped = song_data.drop_duplicates(
        subset = ["artist", "song"], 
        keep = "first"
    )

    song_data_deduped.to_csv(
        "data/songs.csv", 
        sep = "\t", 
        lineterminator = "\n", 
        columns = ["artist", "song"]
    )