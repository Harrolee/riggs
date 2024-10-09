import requests
from bs4 import BeautifulSoup, Comment
from prep_songs_for_scraping import construct_azlyric_urls, get_artist_song

# def save_lyrics(lyrics: str, artist:str, song:str):
#     with open(f"lryics/{artist.replace(' ', '_')}-{song.replace(' ', '_')}.txt", 'w') as f:
#         f.write(lyrics)
def save_lyrics(lyrics: str, url: str):
    with open(f"lyrics/{url[32:-5].replace('/','-')}.txt", 'w') as f:
        f.write(lyrics)

def lyrics_from_setlist(setlist_path):
    artist_song = get_artist_song(setlist_path)
    urls = construct_azlyric_urls(artist_song)

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if "Usage of azlyrics.com content by any third-party lyrics provider is prohibited" in comment:
                div_with_comment = comment.find_parent('div')
                text_with_newlines = div_with_comment.get_text()
                save_lyrics(text_with_newlines, url)


lyrics_from_setlist("data/setlists/testing - Locktoberfest Final.csv")