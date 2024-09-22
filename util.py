import uuid

def get_output_path(lyric, config):
    out = lyric.replace(' ', '')
    out = out[-10] if len(out) > 10 else out
    out = out + str(uuid.uuid4())[:8]
    out = f'data/images/{out}.png'
    return out
