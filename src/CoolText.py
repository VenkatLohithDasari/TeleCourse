import requests
import urllib.parse
import json
from PIL import Image


def split_string(long_string):
    words = long_string.split()
    new_lines = [words[i:i+3] for i in range(0, len(words), 3)]
    return '\r\n'.join([' '.join(line) for line in new_lines])


def getImage(fileName, logoID):
    url = "https://cooltext.com/PostChange"
    form_data = {
        "LogoID": logoID,
        "Text": split_string(fileName),
        "FontSize": 120,
        "FileFormat": 6,
        "BackgroundColor_color": "#FFFFFF"
    }
    parsed_date = urllib.parse.urlencode(form_data)
    server = requests.post(f"{url}?{parsed_date}")
    output = json.loads(server.text)
    newID = output["newId"]
    image_url = requests.utils.quote(
        output["renderLocation"],
        safe=':/()-.'
    )
    img = Image.open(requests.get(image_url, stream=True).raw)
    img.save('image.png')
    return {
        "image": "image.png",
        "newID": newID,
    }
