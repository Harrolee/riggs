# Function to format artist and song for the URL
import csv
import re

def format_artist_name(artist):
    if ',' in artist:
        parts = artist.split(',')
        # Reverse and join with a space, trimming extra whitespace
        artist = ' '.join(reversed([part.strip() for part in parts]))
    return artist.strip()

def get_list_from_csv(csv_file_path):
    songs_artists = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        # Skip the header row
        next(csv_reader)
        for row in csv_reader:
            artist = row[0].strip()
            song = row[1].strip()
            formatted_artist = format_artist_name(artist)
            if formatted_artist and song:
                songs_artists.append((song, formatted_artist))
    return songs_artists

def format_for_url(text):
    # Remove anything that's not a letter or a number
    return re.sub(r'[^a-z0-9]', '', text.lower())


def get_artist_song(setlist_path):
    artist_song = []
    with open(setlist_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            artist, song = row[0].strip(), row[1].strip()
            artist = format_artist_name(artist)
            if artist and song:
                artist_song.append((artist, song))

                artist_url = format_for_url(artist)
                song_url = format_for_url(song)                
                url = f"https://www.azlyrics.com/lyrics/{artist_url}/{song_url}.html"
                
                print(f"{artist} - {song}: {url}")
    return artist_song


def construct_azlyric_urls(artist_song: list) -> list:
    urls = []
    for pair in artist_song:
        artist_url = format_for_url(pair[0])
        song_url = format_for_url(pair[1])                
        urls.append(f"https://www.azlyrics.com/lyrics/{artist_url}/{song_url}.html")
    return urls