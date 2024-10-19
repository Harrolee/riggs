import requests
import fal_client

image_sizes = {
    # https://docs.getimg.ai/reference/postfluxschnelltexttoimage#body-postFluxSchnellTextToImage_width
    # flux image api max dimension size is 1280
    # fb post image display ratio is 2/3
    "post": {"height":768, "width": 1280}
}
class ImageGenerationError(Exception):
    """Custom exception for image generation errors."""
    def __init__(self, status_code, message):
        super().__init__(f"Image generation failed. Status code and message of the request follows:\nStatus Code: {status_code}\nMessage: {message}")
        self.status_code = status_code
        self.message = message

def getimg_generate_image(prompt, config):
    url = "https://api.getimg.ai/v1/flux-schnell/text-to-image"
    # https://docs.getimg.ai/reference/postfluxschnelltexttoimage
    payload = {
        "prompt": prompt,
        "height": image_sizes["post"]["height"],
        "width": image_sizes["post"]["width"],
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


def fal_generate_image(prompt, config):

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs: # type: ignore
                print(log["message"])

    result = fal_client.subscribe(
        "fal-ai/flux/dev",
        arguments={
            "prompt": prompt,
            "image_size": {
                "height": image_sizes["post"]["height"],
                "width": image_sizes["post"]["width"],
            }
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    print(result)
    img = requests.get(result['images'][0]['url']).content
    return img