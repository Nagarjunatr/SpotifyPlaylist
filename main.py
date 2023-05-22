import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# rseponse = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
# web_html = rseponse.text
# soup = BeautifulSoup(web_html, "html.parser")
# all_movies = soup.findAll(name="h3", class_="title")
# movie_titles = [movie.getText() for movie in all_movies]
# movies = movie_titles[::-1]
# with codecs.open("movies.txt", "w",encoding='utf-8', errors='strict') as f:
#     for movie in movies:
#         f.write(f"{movie}\n")


CLIENT_ID = os.environ.get("CLIENTID")
CLIENT_SECRET = os.environ.get("CLIENTSEC")



date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")

soup = BeautifulSoup(response.text, "html.parser")
song_list_li = soup.select(selector="li ul li h3", id="title-of-a-story")
song_names = [song.get_text(strip=True) for song in song_list_li]
print(song_names)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8888/callback", scope="playlist-modify-private", show_dialog=True, cache_path="token.txt"))
user_id = sp.current_user()["id"]


song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#

# print(song_names)

# Private playlist
playlist = sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)