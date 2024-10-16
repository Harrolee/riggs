# https://docs.getimg.ai/reference/postfluxschnelltexttoimage
import requests

class ImageGenerationError(Exception):
    """Custom exception for image generation errors."""
    def __init__(self, status_code, message):
        super().__init__(f"Image generation failed. Status code and message of the request follows:\nStatus Code: {status_code}\nMessage: {message}")
        self.status_code = status_code
        self.message = message

def generate_image(prompt, config):
    url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"

    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "seed": 0,
        "output_format": "png",
        "response_format": "b64"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {config.getimg_token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    if (response.ok):
        b64_image = response.json()['image']
        return b64_image
    else:
            raise ImageGenerationError(response.status_code, response.text)
