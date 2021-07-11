import requests
import time
import json
from collections import defaultdict
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE_DIR = os.path.join(BASE_DIR, 'data')

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    print("Key not found")
    exit

CHANNELS_API_URL = "https://www.googleapis.com/youtube/v3/channels"
PLAYLIST_API_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
OUTPUT_FIELDS = ["video_id", "title", "video_published_at"]
last_video = "Samveda 2021-22 | Day-01 | 10th Class | First Language Kannada | Prose-1 | Yuddha "

channels_params = {
    "key": API_KEY,
    "part": "contentDetails",
}

playlist_params = {
    "key": API_KEY,
    "part": "snippet",
    "maxResults": 50,
}

channel_id = "UCbdMik2cV8pea1jcWdX_CYA"
channels_params.update({"id": channel_id})

r = requests.get(
      CHANNELS_API_URL,
      params=channels_params,
  ).json()

uploads_id = r["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

playlist_params.update({"playlistId": uploads_id})
r = requests.get(
    PLAYLIST_API_URL,
    params=playlist_params,
).json()

YOUTUBE_URL_PREFIX = "https://www.youtube.com/watch?v="

dataset = []
for video in r["items"]:
  if "Samveda 2021-22" in video["snippet"]["title"]  and "Urdu Medium" not in video["snippet"]["title"]:
    title = video["snippet"]["title"]
    date = video["snippet"]["publishedAt"]
    url = YOUTUBE_URL_PREFIX+video["snippet"]["resourceId"]["videoId"]
    dataset.append([date, title, url])

pageToken = r.get("nextPageToken")

done = False
while pageToken:
  playlist_params.update({"pageToken": pageToken})
  r = requests.get(
      PLAYLIST_API_URL,
      params=playlist_params,
  ).json()

  for video in r["items"]:
      if "Samveda 2021-22" in video["snippet"]["title"]  and "Urdu Medium" not in video["snippet"]["title"]:
        title = video["snippet"]["title"]
        date = video["snippet"]["publishedAt"]
        url = YOUTUBE_URL_PREFIX+video["snippet"]["resourceId"]["videoId"]
        # print(date, title, url)
        dataset.append([date, title, url])
      if last_video in title:
        done = True
        break
  if done:
    break
  pageToken = r.get("nextPageToken")
  time.sleep(0.1)

dataset.reverse()

class_list = ["Classes 1-3", "4th Class", "5th Class", "6th Class", "7th Class", "8th Class", "9th Class", "10th Class"]

res = defaultdict(list)
for entry in dataset:
    for standard in class_list:
        if standard in entry[1]:
            res[standard].append(entry)

file_path = os.path.join(DATA_FILE_DIR, 'data.json')
with open(file_path, 'w') as f:
    json.dump(res, f, indent=2)
