from dotenv import dotenv_values
from pathlib import Path

config = dotenv_values(".env")
import os 

if os.environ.get('IS_DOCKER') == 'true':
    config = os.environ


nucklehead_page_id = '297774277014174'
testing_page_id = '394501237087953'

riggs_app_id = '896712469175609'

class AppConfig:
    def __init__(self):
        self.local_lyrics_path = 'lyrics'
        self.local_image_path = 'data/images'
        Path(self.local_image_path).mkdir(exist_ok=True,parents=True)
        self.fb_access_token = config['FB_ACCESS_TOKEN']
        self.fb_app_id = riggs_app_id
        self.fb_app_secret = config['FB_APP_SECRET']
        self.aws_access_key = config['AWS_ACCESS_KEY']
        self.aws_access_token = config['AWS_ACCESS_TOKEN']
        self.aws_s3_bucket = config['AWS_S3_BUCKET']
        # self.getimg_token = config['GETIMG_TOKEN']
        self.predictionguard_token = config['PREDICTIONGUARD_API_KEY']
        if config['TEST'] == 'true':
            self.page_id = testing_page_id
        else:
            self.page_id = nucklehead_page_id
