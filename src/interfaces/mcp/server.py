import asyncio
import json
import time
from datetime import datetime
from typing import Any, Dict, List

from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent
import mcp.server.stdio

from ...core.use_cases.music import MusicService
from ...infrastructure.external.youtube_repository import YouTubeRepository
from ...infrastructure.database.postgres_repository import PostgresRepository

# Initialize services
music_repo = YouTubeRepository()
music_service = MusicService(music_repo)
db_repo = PostgresRepository()

# Create the MCP server
server = Server("mcp-music-api")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_current_time",
            description="Get the current date and time",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="calculate_sum",
            description="Calculate the sum of two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="reverse_string",
            description="Reverse a given string",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The string to reverse"},
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="postgres_query",
            description="Execute a PostgreSQL SELECT query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The SQL SELECT query"},
                    "params": {"type": "array", "items": {"type": "string"}, "description": "Query parameters"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="postgres_execute",
            description="Execute a PostgreSQL INSERT, UPDATE, or DELETE command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The SQL command"},
                    "params": {"type": "array", "items": {"type": "string"}, "description": "Command parameters"},
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="postgres_list_tables",
            description="List all tables in the PostgreSQL database",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="postgres_get_schema",
            description="Get schema information for a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table"},
                },
                "required": ["table_name"],
            },
        ),
        Tool(
            name="youtube_search_music",
            description="Search for music on YouTube Music",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "number", "description": "Max results (default: 10)"},
                    "filter_type": {
                        "type": "string",
                        "description": "Filter: songs, albums, artists, playlists, videos",
                        "enum": ["songs", "albums", "artists", "playlists", "videos"]
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="youtube_get_song_details",
            description="Get detailed information about a specific song",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_id": {"type": "string", "description": "YouTube video ID"},
                },
                "required": ["video_id"],
            },
        ),
        Tool(
            name="youtube_get_artist_details",
            description="Get detailed information about an artist",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel_id": {"type": "string", "description": "Artist Channel ID"},
                },
                "required": ["channel_id"],
            },
        ),
        Tool(
            name="youtube_get_album_details",
            description="Get detailed information about an album",
            inputSchema={
                "type": "object",
                "properties": {
                    "browse_id": {"type": "string", "description": "Album Browse ID"},
                },
                "required": ["browse_id"],
            },
        ),
        Tool(
            name="youtube_get_lyrics",
            description="Get lyrics for a song",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_id": {"type": "string", "description": "YouTube video ID"},
                },
                "required": ["video_id"],
            },
        ),
        Tool(
            name="youtube_download_mp3",
            description="Download a song as MP3 from YouTube",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_id": {"type": "string", "description": "YouTube video ID"},
                    "filename": {"type": "string", "description": "Custom filename"},
                },
                "required": ["video_id"],
            },
        ),
        Tool(
            name="youtube_get_trending",
            description="Get trending music from YouTube Music",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "number", "description": "Max results (default: 20)"},
                },
                "required": [],
            },
        ),
        Tool(
            name="youtube_get_recommendations",
            description="Get music recommendations based on a song",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_id": {"type": "string", "description": "Base video ID"},
                    "limit": {"type": "number", "description": "Max results (default: 10)"},
                },
                "required": ["video_id"],
            },
        ),
        Tool(
            name="youtube_list_downloaded",
            description="List all downloaded MP3 songs",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "get_current_time":
            return [TextContent(type="text", text=f"Current date and time: {datetime.now().isoformat()}")]
        
        elif name == "calculate_sum":
            return [TextContent(type="text", text=f"Sum: {arguments.get('a', 0) + arguments.get('b', 0)}")]
        
        elif name == "reverse_string":
            return [TextContent(type="text", text=f"Reversed: {arguments.get('text', '')[::-1]}")]
        
        # Database Tools
        elif name == "postgres_query":
            results = db_repo.execute_query(arguments.get("query", ""), tuple(arguments.get("params", [])))
            return [TextContent(type="text", text=f"Results: {json.dumps(results, indent=2, default=str)}")]
            
        elif name == "postgres_execute":
            affected = db_repo.execute_command(arguments.get("command", ""), tuple(arguments.get("params", [])))
            return [TextContent(type="text", text=f"Affected rows: {affected}")]
            
        elif name == "postgres_list_tables":
            tables = db_repo.get_tables()
            return [TextContent(type="text", text=f"Tables: {json.dumps(tables, indent=2)}")]
            
        elif name == "postgres_get_schema":
            schema = db_repo.get_table_schema(arguments.get("table_name", ""))
            return [TextContent(type="text", text=f"Schema: {json.dumps(schema, indent=2, default=str)}")]

        # Music Tools
        elif name == "youtube_search_music":
            results = music_service.search_music(
                arguments.get("query", ""), 
                arguments.get("limit", 10),
                arguments.get("filter_type", "songs")
            )
            return [TextContent(type="text", text=f"Results: {json.dumps(results, indent=2, default=str)}")]
            
        elif name == "youtube_get_song_details":
            details = music_service.get_song_details(arguments.get("video_id", ""))
            return [TextContent(type="text", text=f"Details: {json.dumps(details, indent=2, default=str)}")]
            
        elif name == "youtube_get_artist_details":
            details = music_service.get_artist_details(arguments.get("channel_id", ""))
            return [TextContent(type="text", text=f"Details: {json.dumps(details, indent=2, default=str)}")]
            
        elif name == "youtube_get_album_details":
            details = music_service.get_album_details(arguments.get("browse_id", ""))
            return [TextContent(type="text", text=f"Details: {json.dumps(details, indent=2, default=str)}")]
            
        elif name == "youtube_get_lyrics":
            lyrics = music_service.get_lyrics(arguments.get("video_id", ""))
            return [TextContent(type="text", text=f"Lyrics: {json.dumps(lyrics, indent=2, default=str)}")]
            
        elif name == "youtube_download_mp3":
            result = music_service.download_song(arguments.get("video_id", ""), arguments.get("filename"))
            return [TextContent(type="text", text=f"Result: {json.dumps(result, indent=2, default=str)}")]
            
        elif name == "youtube_get_trending":
            results = music_service.get_trending(arguments.get("limit", 20))
            return [TextContent(type="text", text=f"Trending: {json.dumps(results, indent=2, default=str)}")]
            
        elif name == "youtube_get_recommendations":
            results = music_service.get_recommendations(arguments.get("video_id", ""), arguments.get("limit", 10))
            return [TextContent(type="text", text=f"Recommendations: {json.dumps(results, indent=2, default=str)}")]
            
        elif name == "youtube_list_downloaded":
            songs = music_service.get_downloaded_songs()
            return [TextContent(type="text", text=f"Downloaded: {json.dumps(songs, indent=2, default=str)}")]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

@server.list_resources()
async def list_resources() -> List[Dict[str, Any]]:
    return [
        {"uri": "example://system-info", "name": "System Info", "mimeType": "application/json"},
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "example://system-info":
        return json.dumps({"status": "running", "version": "2.0.0"}, indent=2)
    raise ValueError(f"Unknown resource: {uri}")

async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
