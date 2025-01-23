from dotenv import load_dotenv
import os
import base64
from requests import get, post
import json

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
  auth_string = client_id + ":" + client_secret
  auth_bytes = auth_string.encode("utf-8")
  auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

  url = "https://accounts.spotify.com/api/token"
  headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded"
  }
  data = {"grant_type": "client_credentials"}
  result = post(url, headers=headers, data=data)
  json_result = json.loads(result.content)
  token = json_result["access_token"]
  return token

def get_auth_header(token):
  return {"Authorization": "Bearer " + token}

def get_playlist_tracks(token, playlist_id):
  url = f"https://api.spotify.com/v1/playlists/{playlist_id}?fields=tracks.items%28track%28name%29%29"

  headers = get_auth_header(token)

  result = get(url, headers=headers)
  json_result = json.loads(result.content)
  return json_result
  

token = get_token()
playlist_id = "[playlist_id]"
result_raw = get_playlist_tracks(token, playlist_id)
result_str = str(result_raw)


result_out = result_str

result_out = result_str.replace("{'tracks': ", "").replace("{'items': ", "").replace("[{'track': ", "").replace("{'na", "").replace('me\': "', "\n").replace("me': '", "\n").replace("{'track': ", "").replace("'}},", "").replace('"}}, ', "").removesuffix("'}}]}}")

spotify = open("/home/jason/Desktop/spotify.txt", "w")
spotify.write(result_out)
spotify.close()

print(result_out)
