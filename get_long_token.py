"""
Make Automated Posts to Facebook Page
Written by Arul John
Blog Post: https://aruljohn.com/blog/python-automate-facebook-posts/
"""
import requests
from config import AppConfig

# Explorer
# https://developers.facebook.com/tools/explorer

# Variables
version = 'v19.0'

# Your App information

config = AppConfig()
# Get long token
print(f'''
curl -i -X GET "https://graph.facebook.com/{version}/oauth/access_token?grant_type=fb_exchange_token&client_id={config.fb_app_id}&client_secret={config.fb_app_secret}&fb_exchange_token={config.fb_access_token}"
''')
