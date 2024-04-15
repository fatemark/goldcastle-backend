import os
import requests
from datetime import datetime
from requests.exceptions import ReadTimeout

def elevenlabs(text, voice_id):
    elevenlabs_api_key = os.environ['ELEVENLABS_API_KEY']
    words = text.split()[:5]
    first_five_words = "_".join(words)
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create the output file name
    output_file = f"audio/{first_five_words}_{current_datetime}.mp3"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    querystring = {"output_format":"mp3_44100_192"}
    payload = {
        "voice_settings": {
            "similarity_boost": 0.77,
            "stability": 1,
            "style": 0.34,
            "use_speaker_boost": True
        },
        "model_id": "eleven_multilingual_v2",
        "text": text
    }
    headers = {
        "xi-api-key": elevenlabs_api_key,
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        return output_file
    else:
        return None