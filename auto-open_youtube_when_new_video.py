# Auto Open YouTube for new videos of favorite channel

import urllib, json
from selenium import webdriver # pip3 install selenium
import time


def look_for_new_video():
    api_key = "get a key at https://console.developers.google.com"
    channel_id = "UCU5JicSrEM5A63jkJ2QvGYw" # Filipe Deschamps channel

    base_video_url = "https://www.youtube.com/watch?v="
    base_search_url = "https://www.googleapis.com/youtube/v3/search?"

    url = base_search_url + "key={}&channelId={}&part=snippet,id&order=date&maxResults=1".format(api_key, channel_id)

    req = urllib.request.urlopen(url)
    res = json.load(req)

    video_id = res['items'][0]['id']['videoId']

    with open('videoid.json', 'r') as json_file:
        data = json.load(json_file)
        if data['videoId'] != video_id:
            driver = webdriver.Firefox()
            driver.get(base_video_url + video_id)
            video_exists = True

        if video_exists:
            with open('videoid.json', 'w') as json_file:
                data = {'videoId' : video_id}
                json.dump(data, json_file)

try:
    while True:
        look_for_new_video()
        time.sleep(10)
except KeyboardInterrupt:
    print('Stopping...')
    