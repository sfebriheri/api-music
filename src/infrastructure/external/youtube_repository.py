import os
import re
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import ytmusicapi
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

from ...core.use_cases.music import MusicRepository

class YouTubeRepository(MusicRepository):
    def __init__(self):
        self.ytmusic = ytmusicapi.YTMusic()
        self.download_dir = os.getenv('MUSIC_DOWNLOAD_DIR', os.path.expanduser('~/Music'))
        self._ensure_download_dir()
    
    def _ensure_download_dir(self):
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)

    def search(self, query: str, limit: int, filter_type: str) -> List[Dict[str, Any]]:
        try:
            results = self.ytmusic.search(query, filter=filter_type, limit=limit)
            
            parsed_results = []
            for item in results:
                result_type = item.get('resultType', filter_type)
                parsed_item = {'type': result_type}
                
                if result_type in ['song', 'video']:
                    parsed_item.update({
                        'title': item.get('title', 'Unknown'),
                        'artist': item.get('artists', [{}])[0].get('name', 'Unknown'),
                        'album': item.get('album', {}).get('name', 'Unknown'),
                        'duration': item.get('duration', 'Unknown'),
                        'video_id': item.get('videoId', ''),
                        'thumbnail': item.get('thumbnails', [{}])[-1].get('url', ''),
                    })
                elif result_type == 'album':
                    parsed_item.update({
                        'title': item.get('title', 'Unknown'),
                        'artist': item.get('artists', [{}])[0].get('name', 'Unknown'),
                        'year': item.get('year', 'Unknown'),
                        'browse_id': item.get('browseId', ''),
                        'thumbnail': item.get('thumbnails', [{}])[-1].get('url', ''),
                    })
                elif result_type == 'artist':
                    parsed_item.update({
                        'name': item.get('artist', 'Unknown'),
                        'subscribers': item.get('subscribers', 'Unknown'),
                        'browse_id': item.get('browseId', ''),
                        'thumbnail': item.get('thumbnails', [{}])[-1].get('url', ''),
                    })
                elif result_type == 'playlist':
                    parsed_item.update({
                        'title': item.get('title', 'Unknown'),
                        'author': item.get('artists', [{}])[0].get('name', 'Unknown') if item.get('artists') else 'Unknown',
                        'count': item.get('itemCount', 'Unknown'),
                        'browse_id': item.get('browseId', ''),
                        'thumbnail': item.get('thumbnails', [{}])[-1].get('url', ''),
                    })
                
                parsed_results.append(parsed_item)
                
            return parsed_results
        except Exception as e:
            return [{'error': f'Search failed: {str(e)}'}]

    def get_song_details(self, video_id: str) -> Dict[str, Any]:
        try:
            yt_info = self.ytmusic.get_song(video_id)
            yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            
            details = {
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
            
            try:
                watch_playlist = self.ytmusic.get_watch_playlist(videoId=video_id)
                if 'lyrics' in watch_playlist:
                    lyrics_id = watch_playlist['lyrics']
                    lyrics_data = self.ytmusic.get_lyrics(lyrics_id)
                    details['lyrics'] = lyrics_data.get('lyrics', 'No lyrics available')
            except Exception:
                details['lyrics'] = 'Lyrics fetch failed or unavailable'
                
            return details
        except Exception as e:
            return {'error': f'Failed to get song details: {str(e)}'}

    def get_artist_details(self, channel_id: str) -> Dict[str, Any]:
        try:
            artist = self.ytmusic.get_artist(channel_id)
            return {
                'name': artist.get('name', 'Unknown'),
                'description': artist.get('description', ''),
                'views': artist.get('views', ''),
                'subscribers': artist.get('subscribers', ''),
                'thumbnails': artist.get('thumbnails', []),
                'songs': artist.get('songs', {}).get('results', [])[:5],
                'albums': artist.get('albums', {}).get('results', [])[:5],
                'singles': artist.get('singles', {}).get('results', [])[:5]
            }
        except Exception as e:
            return {'error': f'Failed to get artist details: {str(e)}'}

    def get_album_details(self, browse_id: str) -> Dict[str, Any]:
        try:
            album = self.ytmusic.get_album(browse_id)
            return {
                'title': album.get('title', 'Unknown'),
                'artists': album.get('artists', []),
                'year': album.get('year', ''),
                'track_count': album.get('trackCount', 0),
                'duration': album.get('duration', ''),
                'tracks': [
                    {
                        'title': track.get('title', 'Unknown'),
                        'duration': track.get('duration', ''),
                        'video_id': track.get('videoId', ''),
                        'artists': track.get('artists', [])
                    }
                    for track in album.get('tracks', [])
                ],
                'description': album.get('description', '')
            }
        except Exception as e:
            return {'error': f'Failed to get album details: {str(e)}'}

    def get_lyrics(self, video_id: str) -> Dict[str, Any]:
        try:
            watch_playlist = self.ytmusic.get_watch_playlist(videoId=video_id)
            if 'lyrics' in watch_playlist:
                lyrics_id = watch_playlist['lyrics']
                lyrics_data = self.ytmusic.get_lyrics(lyrics_id)
                return {
                    'lyrics': lyrics_data.get('lyrics', 'No lyrics available'),
                    'source': lyrics_data.get('source', 'Unknown')
                }
            return {'error': 'No lyrics found for this song'}
        except Exception as e:
            return {'error': f'Failed to get lyrics: {str(e)}'}

    def get_trending(self, limit: int) -> List[Dict[str, Any]]:
        try:
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

    def get_recommendations(self, video_id: str, limit: int) -> List[Dict[str, Any]]:
        try:
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

    def download_song(self, video_id: str, filename: Optional[str] = None) -> Dict[str, Any]:
        try:
            yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
            audio_stream = yt.streams.filter(only_audio=True).first()
            if not audio_stream:
                return {'error': 'No audio stream available'}
            
            if not filename:
                safe_title = re.sub(r'[^\w\s-]', '', yt.title).strip()
                safe_title = re.sub(r'[-\s]+', '-', safe_title)
                filename = f"{safe_title}.mp3"
            
            if not filename.endswith('.mp3'):
                filename += '.mp3'
            
            filepath = os.path.join(self.download_dir, filename)
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

    def get_downloaded_songs(self) -> List[Dict[str, Any]]:
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
