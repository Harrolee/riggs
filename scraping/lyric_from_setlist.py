import csv
import random
from pathlib import Path


def load_lyrics(song_name: str) -> str:
    song_name = song_name.lower().replace(' ','_')
    with open(f'lyrics/{song_name}.txt', 'r') as f:
        lyrics = f.read()
    return lyrics

def get_random_lyrics(dir_path):
    files = [f for f in Path(dir_path).rglob('*.txt') if f.is_file()]
    if not files:
        return "No .txt files found in the directory."

    selected_file = random.choice(files)
    file_path = str(selected_file)

    with open(file_path, 'r') as file:
        lyrics = file.read()

    return lyrics

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

csv_file_path = 'data/setlists/testing - Locktoberfest Final.csv'
setlist = get_list_from_csv(csv_file_path)

song = setlist[random.randint(0, len(setlist)-1)]

lyrics = load_lyrics("Do I Wanna Know")
