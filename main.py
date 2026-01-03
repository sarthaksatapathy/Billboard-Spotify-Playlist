import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#-------Billboard Scraping


date = input("Which year do you want to travel to? Type the date in YYYY-MM-DD format: ")
year = date.split("-")[0]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/135.0.0.0 Safari/537.36"
}

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(billboard_url, headers=headers)
billboard_html = response.text

soup = BeautifulSoup(billboard_html, "html.parser")
song_tags = soup.find_all("h3", id="title-of-a-story")

songs = [song.getText().strip() for song in song_tags]

print(f"Scraped {len(songs)} songs from Billboard.")


#----- Spotify Authentication


CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        cache_path="token.txt",
        show_dialog=True
    )
)

user_id = sp.current_user()["id"]
print("Authenticated as:", user_id)


#-----Search Spotify for Songs


song_uris = []

for song in songs:
    try:
        result = sp.search(
            q=f"track:{song} year:{year}",
            type="track",
            limit=1
        )
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"'{song}' not found on Spotify. Skipped.")

print(f"Found {len(song_uris)} songs on Spotify.")


#-----Create Playlist & Add Songs

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False
)

playlist_id = playlist["id"]

sp.playlist_add_items(
    playlist_id=playlist_id,
    items=song_uris
)

print("Playlist created and songs added successfully!")
