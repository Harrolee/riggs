import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from generate_img import generate_image, ImageGenerationError

# draw = ImageDraw.Draw(image)
# _, _, w, h = draw.textbbox((0, 0), message, font=font)
# draw.text(((W-w)/2, (H-h)/2), message, font=font, fill=fontColor)

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
    font = ImageFont.truetype('fonts/NotoSans-Italic.ttf', 65)
    d = ImageDraw.Draw(txt)

    text_length = d.textlength(text, font=font)
    balanced_text = [text]
    if text_length > img.width:
        balanced_text = balance_text(text)

    # place text
    y = 10
    for text_line in balanced_text:
        d.text((50, y), text_line, font=font, fill=(148,0,211, 100))
        y+=80

    out = Image.alpha_composite(img, txt)

    out.show()
    # Save the edited image
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
    if tags:
        return f'image for a {genre} song with these tags: {tags} and with this lyric: {lyric}'
    return f'image for a {genre} song with this lyric: {lyric}'

def create_img(lyric, genre, tags, config, output_path):
    prompt = get_prompt(lyric, genre, tags)
    b64_img = generate_image(prompt, config)
    img = decode_b64_image(b64_img, return_image=True)
    text_on_image(img, lyric, output_path)
