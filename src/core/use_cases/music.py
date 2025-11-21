from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..entities.models import Song, Artist, Album, Playlist

class MusicRepository(ABC):
    @abstractmethod
    def search(self, query: str, limit: int, filter_type: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_song_details(self, video_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_artist_details(self, channel_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_album_details(self, browse_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_lyrics(self, video_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_trending(self, limit: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_recommendations(self, video_id: str, limit: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def download_song(self, video_id: str, filename: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_downloaded_songs(self) -> List[Dict[str, Any]]:
        pass

class MusicService:
    def __init__(self, repository: MusicRepository):
        self.repository = repository

    def search_music(self, query: str, limit: int = 10, filter_type: str = 'songs') -> List[Dict[str, Any]]:
        return self.repository.search(query, limit, filter_type)

    def get_song_details(self, video_id: str) -> Dict[str, Any]:
        return self.repository.get_song_details(video_id)

    def get_artist_details(self, channel_id: str) -> Dict[str, Any]:
        return self.repository.get_artist_details(channel_id)

    def get_album_details(self, browse_id: str) -> Dict[str, Any]:
        return self.repository.get_album_details(browse_id)

    def get_lyrics(self, video_id: str) -> Dict[str, Any]:
        return self.repository.get_lyrics(video_id)

    def get_trending(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self.repository.get_trending(limit)

    def get_recommendations(self, video_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        return self.repository.get_recommendations(video_id, limit)

    def download_song(self, video_id: str, filename: Optional[str] = None) -> Dict[str, Any]:
        return self.repository.download_song(video_id, filename)

    def get_downloaded_songs(self) -> List[Dict[str, Any]]:
        return self.repository.get_downloaded_songs()

    @staticmethod
    def create_youtube_service():
        """Factory method to create a MusicService with YouTube repository"""
        from ...infrastructure.external.youtube_repository import YouTubeRepository
        return MusicService(YouTubeRepository())

    @staticmethod
    def create_spotify_service():
        """Factory method to create a MusicService with Spotify repository"""
        from ...infrastructure.external.spotify_repository import SpotifyRepository
        return MusicService(SpotifyRepository())
