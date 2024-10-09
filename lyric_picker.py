import random
from pathlib import Path

def get_random_lyrics(dir_path):
    files = [f for f in Path(dir_path).rglob('*.txt') if f.is_file()]
    if not files:
        return "No .txt files found in the directory."

    selected_file = random.choice(files)
    file_path = str(selected_file)

    with open(file_path, 'r') as file:
        lyrics = file.read()

    return lyrics