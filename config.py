from dotenv import dotenv_values

config = dotenv_values(".env")

nucklehead_page_id = '297774277014174'
testing_page_id = '394501237087953'

riggs_app_id = '896712469175609'

class AppConfig:
    def __init__(self):
        self.local_image_path = 'data/images'

        self.fb_access_token = config['FB_ACCESS_TOKEN']
        self.fb_app_id = riggs_app_id
        self.fb_app_secret = config['FB_APP_SECRET']
        self.aws_access_key = config['AWS_ACCESS_KEY']
        self.aws_access_token = config['AWS_ACCESS_TOKEN']
        self.aws_s3_bucket = config['AWS_S3_BUCKET']
        self.getimg_token = config['GETIMG_TOKEN']

        if config['TEST'] == 'true':
            self.page_id = testing_page_id
        else:
            self.page_id = nucklehead_page_id
