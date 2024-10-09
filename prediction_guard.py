from typing import Callable, TypeVar
from predictionguard import PredictionGuard
import traceback
from pydantic import BaseModel, Field, ValidationError 
from pydantic_core import from_json
from models import SongData


T = TypeVar("T")

prompt_content = {
    "single_lyric": """ You are a mid thirties classic rock DJ. It is your job to select a line from a song for a promotional image.
                                        You must pick a line that resonates with you emotionally and would provide inspiration for an evocative image.
                                        You must select a lyric with fewer than 40 characters so that it can fit in the image. Output only that lyric.
                    """,
    "lyric_tags_genre": """ You are a mid thirties classic rock DJ. It is your job to extract information from a set of song lyrics in order to create a promotional image.
                            You must extract this information:
                            1. a line that resonates with you emotionally and would provide inspiration for an evocative image. You must select a line with fewer than 40 characters so that it can fit in the image.
                            2. the genre of the song
                            3. tags that you think would help the artist create the image
                            
                            You must output that information in json format, like this:
                            {"lyric": "<extracted lyric here>","genre": "<extracted genre here>","tags": ['first_tag', 'second tag', 'third tag', 'etc...']}
                    """,
    "fix_json": """ You are a component in a computer system. It is your role to convert malformed json into correct json.
                    You will recieve two pieces of information:
                    - malformed json
                    - errors that tell you how it is malformed
                    You must output a corrected version of the malformed json. Your output must not change the meaning of the output. Only the structure. 
                """,
    "caption_image": """ You are a mid thirties classic rock DJ. It is your job to devise a witty and emotionally evocative caption for this image.
                        The caption and image will be posted to social media. A successful caption is one that causes people to like or comment on the post.
                """
}

class PredictionGuardInstance:

    def __init__(self, token):
        self.client = PredictionGuard(api_key=token)

    def _get_prompt(self, prompt_key, insert):
        prompts = { 
            "extract_song_info":[
                {
                    "role": "system",
                    "content":  prompt_content["lyric_tags_genre"]
                },
                {
                    "role": "user",
                    "content": f"{insert}"
                }
            ],
            "fix_json": [
                {
                    "role": "system",
                    "content":  prompt_content["fix_json"]
                },
                {
                    "role": "user",
                    "content": f"{insert}"
                }
            ],
            "caption_img": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_content["caption_image"]
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": insert,
                            }
                        }
                    ]
                },
            ]
        } 
        return prompts[prompt_key]

    def getJsonOutput(self, prompt, validate_output: Callable[[dict], T], model="Hermes-2-Pro-Llama-3-8B",limit=5) -> T:
        fail_count = 0
        output = {"valid":False, "content": {}}
        while(not output["valid"] and fail_count<limit):
            result = self.client.chat.completions.create(
                model=model,
                messages=prompt,
                max_tokens=100
            )
            raw_output = result['choices'][0]['message']['content']
            json_output = from_json(raw_output, allow_partial=True)
            try:
                output["content"] = validate_output(json_output)
                output["valid"] = True
            except ValidationError as e:
                errors = []
                print("Validation Error:")
                for error in e.errors():
                    errors.append(f"Field: {error['loc'][0]}, Error: {error['msg']}")
                    print(f"Field: {error['loc'][0]}, Error: {error['msg']}")

                print(f"\nOriginal Traceback Below")
                traceback.print_exc()
                print(f"\nEnd Traceback")

                print("Rejecting output and requesting a retry")
                prompt = self._get_prompt(["fix_json"], f"Malformed json: {json_output}\n\nHow the json is malformed: {errors}")
        if not output['valid']:
            raise ValueError("Couldn't get the json right, even after 5 attempts")
        return output["content"]
    
    def lyric_select(self, lyrics) -> SongData:
        prompt = self._get_prompt("extract_song_info", lyrics)
        songData = self.getJsonOutput(prompt, SongData.model_validate)

        return songData
    
    def caption_image(self, img_url):
        prompt = self._get_prompt("caption_img", img_url)
        caption = # send request with image
    



# print(json.dumps(
#     PredictionGuard_result,
#     sort_keys=True,
#     indent=4,
#     separators=(',', ': ')
# ))




import os
import json
from predictionguard import PredictionGuard

# Set your Prediction Guard token as an environmental variable.
os.environ["PREDICTIONGUARD_API_KEY"] = "<api key>"

client = PredictionGuard()

messages = [

]

result = client.chat.completions.create(
    model="llava-1.5-7b-hf",
    messages=messages
)

print(json.dumps(
    result,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
))


