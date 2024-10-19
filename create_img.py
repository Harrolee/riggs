import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from generate_img import fal_generate_image


fonts = {"opsilon": 'fonts/opsilon-font/Opsilon-xRj8m.ttf', "whatdo": 'fonts/whatdo-font/Whatdo-DYdPR.ttf', 'silvertones': 'fonts/silvertones-font/Silvertones-0vj3z.ttf'}

def balance_text(text: str):
    split_text = text.split()
    word_count = len(split_text)
    balanced_text = [' '.join(split_text[:word_count//2]),' '.join(split_text[word_count//2:])]
    return balanced_text


# assuming no more than 45 characters, spaces included
def text_on_image(img, text: str, output_path):
    img = img.convert("RGBA")

    # create a background for the text so that we can give the text opacity
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    font = ImageFont.truetype(fonts['whatdo'], 65)
    d = ImageDraw.Draw(txt)

    text_length = d.textlength(text, font=font)
    balanced_text = [text]
    if text_length > img.width:
        balanced_text = balance_text(text)

    # calculate the height of the text block
    line_height = 80

    # place text
    y = 10
    padding_top = 0
    padding_bottom = 23
    text_color = (148,0,211)
    text_color = (255,255,255)
    for text_line in balanced_text:
        # Get the bounding box of the text
        bbox = d.textbbox((0, 0), text_line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Draw a semi-transparent black rectangle behind the text
        # d.rectangle([(50 - padding_top, y - padding_top), (50 + text_width + padding_top, y + text_height + padding_bottom)],fill=(0, 0, 0, 150))  # black with 150 opacity

        d.text((50, y), text_line, font=font, fill=(*text_color, 255))
        y+=line_height

    out = Image.alpha_composite(img, txt)
    out.show()
    out.save(output_path)


def decode_b64_image(base64_str: str, output_file_path='', return_image=False):
    # Decode the Base64 string
    image_data = base64.b64decode(base64_str)
    # Create a BytesIO object from the decoded data
    image = BytesIO(image_data)
    # Open the image using Pillow
    img = Image.open(image)

    if not output_file_path == '':
        img.save(output_file_path)
    if return_image:
        return img


def get_prompt(lyric, genre, tags):
    # guard = "Do NOT add words onto the image!"
    if tags and genre:
        return f'image with no words for a {genre} song inspired by these tags: {tags} and by this lyric: "{lyric}"'
    if genre:
        return f'image with no words for a {genre} song inspired by this lyric: "{lyric}"'
    if tags:
        return f'image with no words for a song inspired by these tags: {tags} and by this lyric: "{lyric}"'
    return f'image with no words for a song inspired by this lyric: "{lyric}"'


def create_img(lyric, genre, tags, config, output_path):
    prompt = get_prompt(lyric, genre, tags)
    img_bytes = fal_generate_image(prompt, config)
    image_io = BytesIO(img_bytes)
    # Open the image using Pillow
    img = Image.open(image_io)
    # img = decode_b64_image(b64_img, return_image=True)
    text_on_image(img, lyric, output_path)
