import requests as requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Provide your ID and Secret you can get one here after login and click on "Create an App" button:  https://developer.spotify.com/dashboard/
MY_ID = ''
MY_SECRET = ''
SPOTIPY_REDIRECT_URI = 'https://example.com'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=MY_ID,
        client_secret=MY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

year = input('What year do you want your music to be? Ex. 2010: ')

page = requests.get(f'https://www.billboard.com/charts/hot-100/{year}-07-31')
soup = BeautifulSoup(page.content, 'html.parser')
all_songs = soup.find_all('span', class_='chart-element__information__song')

song_names = [i.decode_contents() for i in all_songs]

song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"top 100 de {year}", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
