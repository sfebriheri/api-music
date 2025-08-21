#!/usr/bin/env python3
"""
YouTube Music Service for MCP Server

Provides YouTube Music search, download, and playlist management capabilities.
"""

import os
import re
import json
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path
import ytmusicapi
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

class YouTubeMusicService:
    """YouTube Music service for searching and downloading music"""
    
    def __init__(self):
        self.ytmusic = ytmusicapi.YTMusic()
        self.download_dir = os.getenv('MUSIC_DOWNLOAD_DIR', os.path.expanduser('~/Music'))
        self._ensure_download_dir()
    
    def _ensure_download_dir(self):
        """Ensure download directory exists"""
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
    
    def search_music(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for music on YouTube Music"""
        try:
            results = self.ytmusic.search(query, filter='songs', limit=limit)
            return [
                {
                    'title': song.get('title', 'Unknown'),
                    'artist': song.get('artists', [{}])[0].get('name', 'Unknown'),
                    'album': song.get('album', {}).get('name', 'Unknown'),
                    'duration': song.get('duration', 'Unknown'),
                    'video_id': song.get('videoId', ''),
                    'thumbnail': song.get('thumbnails', [{}])[-1].get('url', ''),
                    'year': song.get('year', 'Unknown')
                }
                for song in results
            ]
        except Exception as e:
            return [{'error': f'Search failed: {str(e)}'}]
    
    def get_song_details(self, video_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific song"""
        try:
            # Get YouTube Music details
            yt_info = self.ytmusic.get_song(video_id)
            
            # Get YouTube video details
            yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            
            return {
                'title': yt.title,
                'author': yt.author,
                'length': yt.length,
                'views': yt.views,
                'description': yt.description[:200] + '...' if len(yt.description) > 200 else yt.description,
                'publish_date': str(yt.publish_date),
                'thumbnail_url': yt.thumbnail_url,
                'video_id': video_id,
                'music_info': yt_info
            }
        except Exception as e:
            return {'error': f'Failed to get song details: {str(e)}'}
    
    def download_mp3(self, video_id: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """Download a song as MP3"""
        try:
            yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            
            # Get audio stream
            audio_stream = yt.streams.filter(only_audio=True).first()
            if not audio_stream:
                return {'error': 'No audio stream available'}
            
            # Generate filename if not provided
            if not filename:
                safe_title = re.sub(r'[^\w\s-]', '', yt.title).strip()
                safe_title = re.sub(r'[-\s]+', '-', safe_title)
                filename = f"{safe_title}.mp3"
            
            # Ensure filename has .mp3 extension
            if not filename.endswith('.mp3'):
                filename += '.mp3'
            
            filepath = os.path.join(self.download_dir, filename)
            
            # Download the audio
            audio_stream.download(output_path=self.download_dir, filename=filename)
            
            return {
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'title': yt.title,
                'author': yt.author,
                'size_mb': round(os.path.getsize(filepath) / (1024 * 1024), 2)
            }
        except VideoUnavailable:
            return {'error': 'Video is unavailable or private'}
        except RegexMatchError:
            return {'error': 'Invalid video ID'}
        except Exception as e:
            return {'error': f'Download failed: {str(e)}'}
    
    def download_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Download all songs from a playlist"""
        try:
            # Get playlist information
            playlist = self.ytmusic.get_playlist(playlist_id)
            tracks = playlist.get('tracks', [])
            
            if not tracks:
                return {'error': 'No tracks found in playlist'}
            
            results = []
            successful = 0
            failed = 0
            
            for track in tracks:
                video_id = track.get('videoId')
                if video_id:
                    result = self.download_mp3(video_id)
                    if result.get('success'):
                        successful += 1
                        results.append({
                            'title': track.get('title', 'Unknown'),
                            'status': 'success',
                            'filename': result.get('filename')
                        })
                    else:
                        failed += 1
                        results.append({
                            'title': track.get('title', 'Unknown'),
                            'status': 'failed',
                            'error': result.get('error')
                        })
            
            return {
                'success': True,
                'playlist_name': playlist.get('name', 'Unknown'),
                'total_tracks': len(tracks),
                'successful_downloads': successful,
                'failed_downloads': failed,
                'results': results
            }
        except Exception as e:
            return {'error': f'Playlist download failed: {str(e)}'}
    
    def get_trending_music(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get trending music from YouTube Music"""
        try:
            # Get trending songs
            trending = self.ytmusic.get_charts(country='US')
            songs = trending.get('songs', [])[:limit]
            
            return [
                {
                    'title': song.get('title', 'Unknown'),
                    'artist': song.get('artists', [{}])[0].get('name', 'Unknown'),
                    'album': song.get('album', {}).get('name', 'Unknown'),
                    'duration': song.get('duration', 'Unknown'),
                    'video_id': song.get('videoId', ''),
                    'thumbnail': song.get('thumbnails', [{}])[-1].get('url', ''),
                    'rank': idx + 1
                }
                for idx, song in enumerate(songs)
            ]
        except Exception as e:
            return [{'error': f'Failed to get trending music: {str(e)}'}]
    
    def get_recommendations(self, video_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get music recommendations based on a song"""
        try:
            # Get related videos
            yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            related_videos = yt.related_videos[:limit]
            
            recommendations = []
            for video in related_videos:
                try:
                    recommendations.append({
                        'title': video.title,
                        'author': video.author,
                        'length': video.length,
                        'views': video.views,
                        'video_id': video.video_id,
                        'thumbnail_url': video.thumbnail_url
                    })
                except:
                    continue
            
            return recommendations
        except Exception as e:
            return [{'error': f'Failed to get recommendations: {str(e)}'}]
    
    def get_downloaded_songs(self) -> List[Dict[str, Any]]:
        """Get list of downloaded songs"""
        try:
            songs = []
            for file in os.listdir(self.download_dir):
                if file.endswith('.mp3'):
                    filepath = os.path.join(self.download_dir, file)
                    stat = os.stat(filepath)
                    songs.append({
                        'filename': file,
                        'size_mb': round(stat.st_size / (1024 * 1024), 2),
                        'modified': stat.st_mtime,
                        'filepath': filepath
                    })
            
            return sorted(songs, key=lambda x: x['modified'], reverse=True)
        except Exception as e:
            return [{'error': f'Failed to get downloaded songs: {str(e)}'}]

# Global instance
youtube_music = YouTubeMusicService()
