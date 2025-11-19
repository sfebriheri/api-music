from src.infrastructure.external.youtube_repository import YouTubeRepository
from src.core.use_cases.music import MusicService

# Initialize service
repo = YouTubeRepository()
youtube_music = MusicService(repo)
import json

def print_result(name, result):
    print(f"\n=== {name} ===")
    print(json.dumps(result, indent=2, default=str))

def test_features():
    print("Starting verification of new features...")

    # 1. Search for an Artist
    print("\n1. Searching for artist 'Radiohead'...")
    artist_results = youtube_music.search_music("Radiohead", limit=1, filter_type="artists")
    print_result("Artist Search Results", artist_results)
    
    if not artist_results or 'browse_id' not in artist_results[0]:
        print("Failed to find artist or browse_id")
        return

    artist_id = artist_results[0]['browse_id']
    print(f"Found Artist ID: {artist_id}")

    # 2. Get Artist Details
    print(f"\n2. Getting details for artist {artist_id}...")
    artist_details = youtube_music.get_artist_details(artist_id)
    # Truncate for display
    if 'songs' in artist_details:
        artist_details['songs'] = f"Found {len(artist_details['songs'])} songs"
    if 'albums' in artist_details:
        artist_details['albums'] = f"Found {len(artist_details['albums'])} albums"
    print_result("Artist Details", artist_details)

    # 3. Search for an Album
    print("\n3. Searching for album 'OK Computer'...")
    album_results = youtube_music.search_music("OK Computer", limit=1, filter_type="albums")
    print_result("Album Search Results", album_results)

    if not album_results or 'browse_id' not in album_results[0]:
        print("Failed to find album or browse_id")
        return

    album_id = album_results[0]['browse_id']
    print(f"Found Album ID: {album_id}")

    # 4. Get Album Details
    print(f"\n4. Getting details for album {album_id}...")
    album_details = youtube_music.get_album_details(album_id)
    # Truncate tracks
    if 'tracks' in album_details:
        album_details['tracks'] = f"Found {len(album_details['tracks'])} tracks"
    print_result("Album Details", album_details)

    # 5. Get Lyrics (using a known song or search)
    print("\n5. Searching for song 'Bohemian Rhapsody' to test lyrics...")
    song_results = youtube_music.search_music("Bohemian Rhapsody", limit=1, filter_type="songs")
    
    if song_results and 'video_id' in song_results[0]:
        video_id = song_results[0]['video_id']
        print(f"Found Video ID: {video_id}")
        
        print(f"Getting lyrics for {video_id}...")
        lyrics = youtube_music.get_lyrics(video_id)
        print_result("Lyrics", lyrics)
    else:
        print("Failed to find song for lyrics test")

if __name__ == "__main__":
    test_features()
