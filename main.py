import requests
import os
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

billboard_url = "https://www.billboard.com/charts/hot-100/"

year = int(input("Which year's best songs do you want to add? "))
month = int(input(f"Which month's songs of {year} do you want to add? "))
day = int(input(f"Which day's songs of {year}-{month} do you want to add? "))

response = requests.get(f"{billboard_url}{year}-{month}-{day}/")
billboard_html = response.text
soup = BeautifulSoup(billboard_html, "html.parser")
top_song = soup.find(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
song_names = [top_song.getText().strip()]
song_names += [tag.getText().strip() for tag in soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")]

# with open(".cache") as file:
#     data = file.read()
#     token = eval(data)["access_token"]

scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIFY_CLIENT_ID"],
                                               client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
                                               redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
                                               scope=scope))
user = os.environ["SPOTIFY_USERNAME"]
user_data = sp.user(user)
print("Hello", user_data["display_name"])
playlist_name = 'New Playlist'
playlist_id = sp.user_playlist_create(user, name=playlist_name, description="Created with API")["id"]

songs_uri = []
for song in song_names:
    result = sp.search(f"track: {song} year: 2021", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
    except IndexError:
        continue
    else:
        songs_uri.append(uri)

sp.playlist_add_items(playlist_id, songs_uri)
