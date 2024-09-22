import requests
from config import AppConfig

# Explorer
# https://developers.facebook.com/tools/explorer

# Variables
version = 'v20.0'

# Your App information

config = AppConfig()

def post_message(message):
    baseurl = f'https://graph.facebook.com/{version}/{config.page_id}/feed'
    payload = {
        'message': message,
        'access_token': config.fb_access_token
    }
    res = requests.post(baseurl, data=payload, timeout=10)
    return(res.text)

def post_url(message, url):
    baseurl = f'https://graph.facebook.com/{version}/{config.page_id}/feed'
    payload = {
        'message': message,
        'link': url,
        'access_token': config.fb_access_token
    }
    res = requests.post(baseurl, data=payload, timeout=10)
    return(res.text)

def post_image(image_url, message):
    '''
    Post an image with a caption
    '''
    baseurl = f'https://graph.facebook.com/{version}/{config.page_id}/photos'
    payload = {
        'message': message,
        'url': image_url,
        'published': True,
        'access_token': config.fb_access_token
    }
    # Make Facebook post on your Page
    res = requests.post(baseurl, data=payload, timeout=10)
    return(res.text)
