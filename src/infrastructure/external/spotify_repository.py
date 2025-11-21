import os
from typing import List, Dict, Any, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from ...core.use_cases.music import MusicRepository


class SpotifyRepository(MusicRepository):
    def __init__(self):
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise ValueError("Spotify credentials not found in environment variables")

        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.spotify = spotipy.Spotify(auth_manager=auth_manager)

    def search(self, query: str, limit: int, filter_type: str) -> List[Dict[str, Any]]:
        """Search Spotify for tracks, artists, albums, or playlists"""
        try:
            # Map filter_type to Spotify search types
            search_type_map = {
                'songs': 'track',
                'track': 'track',
                'artists': 'artist',
                'artist': 'artist',
                'albums': 'album',
                'album': 'album',
                'playlists': 'playlist',
                'playlist': 'playlist'
            }

            search_type = search_type_map.get(filter_type, 'track')
            results = self.spotify.search(q=query, type=search_type, limit=limit)

            parsed_results = []

            if search_type == 'track':
                tracks = results.get('tracks', {}).get('items', [])
                for track in tracks:
                    parsed_results.append({
                        'type': 'song',
                        'title': track.get('name', 'Unknown'),
                        'artist': track['artists'][0].get('name', 'Unknown') if track.get('artists') else 'Unknown',
                        'album': track.get('album', {}).get('name', 'Unknown'),
                        'duration': track.get('duration_ms', 0),
                        'track_id': track.get('id', ''),
                        'uri': track.get('uri', ''),
                        'thumbnail': track.get('album', {}).get('images', [{}])[0].get('url', ''),
                        'popularity': track.get('popularity', 0),
                        'explicit': track.get('explicit', False)
                    })

            elif search_type == 'artist':
                artists = results.get('artists', {}).get('items', [])
                for artist in artists:
                    parsed_results.append({
                        'type': 'artist',
                        'name': artist.get('name', 'Unknown'),
                        'artist_id': artist.get('id', ''),
                        'uri': artist.get('uri', ''),
                        'followers': artist.get('followers', {}).get('total', 0),
                        'genres': artist.get('genres', []),
                        'thumbnail': artist.get('images', [{}])[0].get('url', '') if artist.get('images') else '',
                        'popularity': artist.get('popularity', 0)
                    })

            elif search_type == 'album':
                albums = results.get('albums', {}).get('items', [])
                for album in albums:
                    parsed_results.append({
                        'type': 'album',
                        'title': album.get('name', 'Unknown'),
                        'artist': album['artists'][0].get('name', 'Unknown') if album.get('artists') else 'Unknown',
                        'album_id': album.get('id', ''),
                        'uri': album.get('uri', ''),
                        'release_date': album.get('release_date', 'Unknown'),
                        'total_tracks': album.get('total_tracks', 0),
                        'thumbnail': album.get('images', [{}])[0].get('url', ''),
                        'popularity': album.get('popularity', 0)
                    })

            elif search_type == 'playlist':
                playlists = results.get('playlists', {}).get('items', [])
                for playlist in playlists:
                    parsed_results.append({
                        'type': 'playlist',
                        'title': playlist.get('name', 'Unknown'),
                        'owner': playlist.get('owner', {}).get('display_name', 'Unknown'),
                        'playlist_id': playlist.get('id', ''),
                        'uri': playlist.get('uri', ''),
                        'track_count': playlist.get('tracks', {}).get('total', 0),
                        'thumbnail': playlist.get('images', [{}])[0].get('url', '') if playlist.get('images') else '',
                        'description': playlist.get('description', '')
                    })

            return parsed_results
        except Exception as e:
            return [{'error': f'Search failed: {str(e)}'}]

    def get_song_details(self, track_id: str) -> Dict[str, Any]:
        """Get detailed information about a track"""
        try:
            track = self.spotify.track(track_id)
            audio_features = self.spotify.audio_features(track_id)[0]

            details = {
                'title': track.get('name', 'Unknown'),
                'artist': track['artists'][0].get('name', 'Unknown') if track.get('artists') else 'Unknown',
                'album': track.get('album', {}).get('name', 'Unknown'),
                'duration_ms': track.get('duration_ms', 0),
                'track_id': track.get('id', ''),
                'uri': track.get('uri', ''),
                'thumbnail': track.get('album', {}).get('images', [{}])[0].get('url', ''),
                'popularity': track.get('popularity', 0),
                'explicit': track.get('explicit', False),
                'release_date': track.get('album', {}).get('release_date', 'Unknown'),
                'artists': [{'name': artist.get('name'), 'id': artist.get('id')} for artist in track.get('artists', [])],
                'external_urls': track.get('external_urls', {}),
                'audio_features': {
                    'danceability': audio_features.get('danceability') if audio_features else None,
                    'energy': audio_features.get('energy') if audio_features else None,
                    'key': audio_features.get('key') if audio_features else None,
                    'loudness': audio_features.get('loudness') if audio_features else None,
                    'mode': audio_features.get('mode') if audio_features else None,
                    'speechiness': audio_features.get('speechiness') if audio_features else None,
                    'acousticness': audio_features.get('acousticness') if audio_features else None,
                    'instrumentalness': audio_features.get('instrumentalness') if audio_features else None,
                    'liveness': audio_features.get('liveness') if audio_features else None,
                    'valence': audio_features.get('valence') if audio_features else None,
                    'tempo': audio_features.get('tempo') if audio_features else None,
                } if audio_features else {}
            }

            return details
        except Exception as e:
            return {'error': f'Failed to get track details: {str(e)}'}

    def get_artist_details(self, artist_id: str) -> Dict[str, Any]:
        """Get detailed information about an artist"""
        try:
            artist = self.spotify.artist(artist_id)
            albums = self.spotify.artist_albums(artist_id, limit=5)
            top_tracks = self.spotify.artist_top_tracks(artist_id)

            return {
                'name': artist.get('name', 'Unknown'),
                'artist_id': artist.get('id', ''),
                'uri': artist.get('uri', ''),
                'followers': artist.get('followers', {}).get('total', 0),
                'genres': artist.get('genres', []),
                'thumbnail': artist.get('images', [{}])[0].get('url', '') if artist.get('images') else '',
                'popularity': artist.get('popularity', 0),
                'external_urls': artist.get('external_urls', {}),
                'albums': [
                    {
                        'title': album.get('name', 'Unknown'),
                        'album_id': album.get('id', ''),
                        'release_date': album.get('release_date', ''),
                        'total_tracks': album.get('total_tracks', 0)
                    }
                    for album in albums.get('items', [])
                ],
                'top_songs': [
                    {
                        'title': track.get('name', 'Unknown'),
                        'track_id': track.get('id', ''),
                        'popularity': track.get('popularity', 0)
                    }
                    for track in top_tracks.get('tracks', [])
                ]
            }
        except Exception as e:
            return {'error': f'Failed to get artist details: {str(e)}'}

    def get_album_details(self, album_id: str) -> Dict[str, Any]:
        """Get detailed information about an album"""
        try:
            album = self.spotify.album(album_id)
            tracks = self.spotify.album_tracks(album_id)

            return {
                'title': album.get('name', 'Unknown'),
                'artists': [{'name': artist.get('name'), 'id': artist.get('id')} for artist in album.get('artists', [])],
                'album_id': album.get('id', ''),
                'uri': album.get('uri', ''),
                'release_date': album.get('release_date', 'Unknown'),
                'total_tracks': album.get('total_tracks', 0),
                'thumbnail': album.get('images', [{}])[0].get('url', ''),
                'popularity': album.get('popularity', 0),
                'label': album.get('label', 'Unknown'),
                'genres': album.get('genres', []),
                'tracks': [
                    {
                        'title': track.get('name', 'Unknown'),
                        'track_id': track.get('id', ''),
                        'duration_ms': track.get('duration_ms', 0),
                        'track_number': track.get('track_number', 0),
                        'artists': [{'name': artist.get('name')} for artist in track.get('artists', [])]
                    }
                    for track in tracks.get('items', [])
                ]
            }
        except Exception as e:
            return {'error': f'Failed to get album details: {str(e)}'}

    def get_lyrics(self, track_id: str) -> Dict[str, Any]:
        """Get lyrics for a track (Spotify doesn't provide lyrics via API)"""
        try:
            # Spotify API doesn't directly provide lyrics
            # We can search for lyrics using the track title and artist
            track = self.spotify.track(track_id)
            title = track.get('name', '')
            artist = track['artists'][0].get('name', '') if track.get('artists') else ''

            return {
                'note': 'Spotify API does not provide lyrics directly',
                'track_id': track_id,
                'title': title,
                'artist': artist,
                'suggestion': f'Search for lyrics using: "{title}" by "{artist}" on a lyrics service'
            }
        except Exception as e:
            return {'error': f'Failed to get lyrics info: {str(e)}'}

    def get_trending(self, limit: int) -> List[Dict[str, Any]]:
        """Get trending/popular tracks"""
        try:
            # Get featured playlists which typically contain trending tracks
            playlists = self.spotify.featured_playlists(limit=1)
            featured_playlist_id = playlists['playlists']['items'][0]['id']

            # Get tracks from the featured playlist
            playlist_tracks = self.spotify.playlist_tracks(featured_playlist_id, limit=limit)

            trending = []
            for idx, item in enumerate(playlist_tracks.get('items', [])):
                track = item.get('track', {})
                if track:
                    trending.append({
                        'title': track.get('name', 'Unknown'),
                        'artist': track['artists'][0].get('name', 'Unknown') if track.get('artists') else 'Unknown',
                        'album': track.get('album', {}).get('name', 'Unknown'),
                        'duration_ms': track.get('duration_ms', 0),
                        'track_id': track.get('id', ''),
                        'uri': track.get('uri', ''),
                        'thumbnail': track.get('album', {}).get('images', [{}])[0].get('url', ''),
                        'popularity': track.get('popularity', 0),
                        'rank': idx + 1
                    })

            return trending
        except Exception as e:
            return [{'error': f'Failed to get trending tracks: {str(e)}'}]

    def get_recommendations(self, track_id: str, limit: int) -> List[Dict[str, Any]]:
        """Get recommendations based on a track"""
        try:
            recommendations = self.spotify.recommendations(seed_tracks=[track_id], limit=limit)

            recs = []
            for track in recommendations.get('tracks', []):
                recs.append({
                    'title': track.get('name', 'Unknown'),
                    'artist': track['artists'][0].get('name', 'Unknown') if track.get('artists') else 'Unknown',
                    'album': track.get('album', {}).get('name', 'Unknown'),
                    'duration_ms': track.get('duration_ms', 0),
                    'track_id': track.get('id', ''),
                    'uri': track.get('uri', ''),
                    'thumbnail': track.get('album', {}).get('images', [{}])[0].get('url', ''),
                    'popularity': track.get('popularity', 0)
                })

            return recs
        except Exception as e:
            return [{'error': f'Failed to get recommendations: {str(e)}'}]

    def download_song(self, track_id: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Download a song from Spotify (limited functionality)
        Note: Spotify doesn't allow direct downloads via API due to DRM protection
        """
        try:
            track = self.spotify.track(track_id)
            return {
                'error': 'Direct download not supported',
                'reason': 'Spotify has DRM protection and does not allow programmatic downloads',
                'track_info': {
                    'title': track.get('name', 'Unknown'),
                    'artist': track['artists'][0].get('name', 'Unknown') if track.get('artists') else 'Unknown',
                    'uri': track.get('uri', ''),
                    'external_urls': track.get('external_urls', {})
                },
                'alternative': 'Use Spotify Desktop or Web app to download tracks for offline listening'
            }
        except Exception as e:
            return {'error': f'Failed to get track info: {str(e)}'}

    def get_downloaded_songs(self) -> List[Dict[str, Any]]:
        """
        Get downloaded songs (not applicable for Spotify)
        Spotify doesn't support programmatic downloads
        """
        return {
            'message': 'Spotify does not support programmatic downloads',
            'alternative': 'Use Spotify Premium\'s offline download feature in the app'
        }
