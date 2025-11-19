from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Song:
    title: str
    video_id: str
    artist: str = "Unknown"
    album: str = "Unknown"
    duration: str = "Unknown"
    thumbnail: str = ""
    year: str = "Unknown"
    lyrics: Optional[str] = None
    
@dataclass
class Artist:
    name: str
    browse_id: str
    subscribers: str = "Unknown"
    thumbnail: str = ""
    description: str = ""
    songs: List[Dict[str, Any]] = field(default_factory=list)
    albums: List[Dict[str, Any]] = field(default_factory=list)
    singles: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class Album:
    title: str
    browse_id: str
    artist: str = "Unknown"
    year: str = "Unknown"
    thumbnail: str = ""
    tracks: List[Dict[str, Any]] = field(default_factory=list)
    description: str = ""

@dataclass
class Playlist:
    title: str
    browse_id: str
    author: str = "Unknown"
    count: str = "Unknown"
    thumbnail: str = ""
