from config import AppConfig
from lyric_picker import get_random_lyrics
from upload_image import upload_to_aws
from create_img import create_img
from util import get_output_path
from post_to_fb_page import post_image
from prediction_guard import PredictionGuardInstance
from datetime import date
import random

config = AppConfig()

def new_image(song_data): 
    image_path = get_output_path(song_data.lyric, config)
    create_img(song_data.lyric, song_data.genre, song_data.tags, config, image_path)
    yyyy_mm_dd = str(date.today())
    s3_url = upload_to_aws(image_path, f'generated_images/{yyyy_mm_dd}', config)
    if s3_url:
        print(f"File uploaded successfully. Accessible at: {s3_url}")
    else:
        print("File upload failed.")
    return s3_url


def safe_image_gen(song_data, threshold=5):
    attempt = 0
    unsafe = True
    while unsafe:
        if attempt > threshold:
            print(f"image regen attempt #{attempt}")
        s3_url = new_image(song_data)
        unsafe = pg.unsafe_image(s3_url)
    return s3_url # type: ignore


pg = PredictionGuardInstance(config.predictionguard_token)
song_data = pg.lyric_select(get_random_lyrics(config.local_lyrics_path))
song_data.lyric = song_data.lyric.lower()
s3_url = safe_image_gen(song_data)
# caption = pg.caption_image(s3_url) captioning is beyong the ability of llava 1.5
captions = ["Name this song!", 
            "Where were you when you heard this song for the first time?", 
            "Best place to hear this song?",
            "Feel like this song was written for you?",
            "One line, endless emotions",
            "What does this song make you think of?",
            "Can you hear the nostalgia?",
            "What does this lyric remind you of?",
            "Vibin'",
            "Who does this song remind you of?"]

random_caption = random.choice(captions)

result = post_image(s3_url, f"\n{random_caption} \n\nHear it at our next show: https://www.facebook.com/profile.php?id=61566196652037&sk=events") # to fb page
print(result)