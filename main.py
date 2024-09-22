from config import AppConfig
from upload_image import upload_to_aws
from create_img import create_img
from util import get_output_path
from post_to_fb_page import post_image

config = AppConfig()

# song = pick_song() # from repertoire

# lyric = pick_lyric(song) # llm finds most evocative lyric


lyric = "I woke up alone staring at the ceiling"
genre = 'pop'
tags = ''.join(['drag queen', 'fun', 'bubblegum', 'midwest princess'])
output_path = get_output_path(lyric, config)

# create image and put text in it
create_img(lyric, genre, tags, config, output_path)

s3_url = upload_to_aws(output_path, 'generated_images', config)
if s3_url:
    print(f"File uploaded successfully. Accessible at: {s3_url}")
else:
    print("File upload failed.")

result = post_image(s3_url, "message containing information about an upcoming event, with some witty relation to the selected lyric") # to fb page
print(result)
