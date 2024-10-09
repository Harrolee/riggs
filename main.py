from config import AppConfig
from lyric_picker import get_random_lyrics
from upload_image import upload_to_aws
from create_img import create_img
from util import get_output_path
from post_to_fb_page import post_image
from prediction_guard import PredictionGuardInstance

config = AppConfig()

pg = PredictionGuardInstance(config.predictionguard_token)

song_data = pg.lyric_select(get_random_lyrics(config.local_lyrics_path))

image_path = get_output_path(song_data.lyric, config)

create_img(song_data.lyric, song_data.genre, song_data.tags, config, image_path)

s3_url = upload_to_aws(image_path, 'generated_images', config)
if s3_url:
    print(f"File uploaded successfully. Accessible at: {s3_url}")
else:
    print("File upload failed.")

caption = pg.caption_image(s3_url)

result = post_image(s3_url, f"\n{caption} \n\nFind our next show here: https://www.facebook.com/profile.php?id=61566196652037&sk=events") # to fb page