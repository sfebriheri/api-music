#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server Example in Python

This server demonstrates how to create an MCP server with tools and resources,
including PostgreSQL database integration.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Any, Dict, List

from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent, PromptMessage
import mcp.server.stdio

from database_config import db_manager
from youtube_music_service import youtube_music


# Create the MCP server
server = Server("example-mcp-server")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_current_time",
            description="Get the current date and time",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="calculate_sum",
            description="Calculate the sum of two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    },
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
                    "text": {
                        "type": "string",
                        "description": "The string to reverse",
                    },
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
                    "query": {
                        "type": "string",
                        "description": "The SQL SELECT query to execute",
                    },
                    "params": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Query parameters (optional)",
                    },
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
                    "command": {
                        "type": "string",
                        "description": "The SQL command to execute",
                    },
                    "params": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Command parameters (optional)",
                    },
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="postgres_list_tables",
            description="List all tables in the PostgreSQL database",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="postgres_get_schema",
            description="Get schema information for a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to get schema for",
                    },
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
                    "query": {
                        "type": "string",
                        "description": "Search query for music",
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results (default: 10)",
                    },
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
                    "video_id": {
                        "type": "string",
                        "description": "YouTube video ID",
                    },
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
                    "video_id": {
                        "type": "string",
                        "description": "YouTube video ID to download",
                    },
                    "filename": {
                        "type": "string",
                        "description": "Custom filename for the MP3 (optional)",
                    },
                },
                "required": ["video_id"],
            },
        ),
        Tool(
            name="youtube_download_playlist",
            description="Download all songs from a YouTube playlist as MP3s",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {
                        "type": "string",
                        "description": "YouTube playlist ID",
                    },
                },
                "required": ["playlist_id"],
            },
        ),
        Tool(
            name="youtube_get_trending",
            description="Get trending music from YouTube Music",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of trending songs (default: 20)",
                    },
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
                    "video_id": {
                        "type": "string",
                        "description": "YouTube video ID to base recommendations on",
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of recommendations (default: 10)",
                    },
                },
                "required": ["video_id"],
            },
        ),
        Tool(
            name="youtube_list_downloaded",
            description="List all downloaded MP3 songs",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    if name == "get_current_time":
        now = datetime.now()
        return [TextContent(type="text", text=f"Current date and time: {now.isoformat()}")]

    elif name == "calculate_sum":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        sum_result = a + b
        return [TextContent(type="text", text=f"The sum of {a} and {b} is {sum_result}")]

    elif name == "reverse_string":
        text = arguments.get("text", "")
        reversed_text = text[::-1]
        return [TextContent(type="text", text=f'Reversed string: "{reversed_text}"')]

    elif name == "postgres_query":
        query = arguments.get("query", "")
        params = arguments.get("params", [])

        try:
            results = db_manager.execute_query(query, tuple(params) if params else None)
            return [TextContent(type="text", text=f"Query executed successfully. Results: {json.dumps(results, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Query failed: {str(e)}")]

    elif name == "postgres_execute":
        command = arguments.get("command", "")
        params = arguments.get("params", [])

        try:
            affected_rows = db_manager.execute_command(command, tuple(params) if params else None)
            return [TextContent(type="text", text=f"Command executed successfully. Affected rows: {affected_rows}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Command failed: {str(e)}")]

    elif name == "postgres_list_tables":
        try:
            tables = db_manager.get_tables()
            return [TextContent(type="text", text=f"Database tables: {json.dumps(tables, indent=2)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Failed to list tables: {str(e)}")]

    elif name == "postgres_get_schema":
        table_name = arguments.get("table_name", "")

        try:
            schema = db_manager.get_table_schema(table_name)
            return [TextContent(type="text", text=f"Schema for table '{table_name}': {json.dumps(schema, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Failed to get schema for table '{table_name}': {str(e)}")]

    elif name == "youtube_search_music":
        query = arguments.get("query", "")
        limit = arguments.get("limit", 10)

        try:
            results = youtube_music.search_music(query, limit)
            return [TextContent(type="text", text=f"Music search results for '{query}': {json.dumps(results, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Music search failed: {str(e)}")]

    elif name == "youtube_get_song_details":
        video_id = arguments.get("video_id", "")

        try:
            details = youtube_music.get_song_details(video_id)
            return [TextContent(type="text", text=f"Song details for {video_id}: {json.dumps(details, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Failed to get song details: {str(e)}")]

    elif name == "youtube_download_mp3":
        video_id = arguments.get("video_id", "")
        filename = arguments.get("filename")

        try:
            result = youtube_music.download_mp3(video_id, filename)
            return [TextContent(type="text", text=f"MP3 download result: {json.dumps(result, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"MP3 download failed: {str(e)}")]

    elif name == "youtube_download_playlist":
        playlist_id = arguments.get("playlist_id", "")

        try:
            result = youtube_music.download_playlist(playlist_id)
            return [TextContent(type="text", text=f"Playlist download result: {json.dumps(result, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Playlist download failed: {str(e)}")]

    elif name == "youtube_get_trending":
        limit = arguments.get("limit", 20)

        try:
            results = youtube_music.get_trending_music(limit)
            return [TextContent(type="text", text=f"Trending music: {json.dumps(results, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Failed to get trending music: {str(e)}")]

    elif name == "youtube_get_recommendations":
        video_id = arguments.get("video_id", "")
        limit = arguments.get("limit", 10)

        try:
            results = youtube_music.get_recommendations(video_id, limit)
            return [TextContent(type="text", text=f"Music recommendations: {json.dumps(results, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Failed to get recommendations: {str(e)}")]

    elif name == "youtube_list_downloaded":
        try:
            songs = youtube_music.get_downloaded_songs()
            return [TextContent(type="text", text=f"Downloaded songs: {json.dumps(songs, indent=2, default=str)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Failed to list downloaded songs: {str(e)}")]

    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def list_resources() -> List[Dict[str, Any]]:
    """List available resources."""
    return [
        {
            "uri": "example://system-info",
            "name": "System Information",
            "description": "Basic system information and metadata",
            "mimeType": "application/json",
        },
        {
            "uri": "example://sample-data",
            "name": "Sample Data",
            "description": "Example data for testing purposes",
            "mimeType": "application/json",
        },
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Handle resource reading."""
    if uri == "example://system-info":
        try:
            tables = db_manager.get_tables()
            db_status = "Connected"
        except Exception as e:
            db_status = f"Disconnected: {str(e)}"
            tables = []

        info = {
            "server_name": "Example MCP Server with PostgreSQL and YouTube Music",
            "version": "1.0.0",
            "capabilities": ["tools", "resources", "postgres_integration", "youtube_music_integration"],
            "uptime": time.time(),  # Process start time approximation
            "database_status": db_status,
            "database_tables_count": len(tables),
            "available_tables": tables[:10] if tables else [],  # Show first 10 tables
            "youtube_music_status": "Available",
            "total_tools": 15,  # 7 original + 8 new YouTube tools
        }
        return json.dumps(info, indent=2)

    elif uri == "example://sample-data":
        data = {
            "items": [
                {"id": 1, "name": "Item 1", "value": 100},
                {"id": 2, "name": "Item 2", "value": 200},
                {"id": 3, "name": "Item 3", "value": 300},
            ],
            "total": 600,
            "count": 3,
        }
        return json.dumps(data, indent=2)

    else:
        raise ValueError(f"Unknown resource: {uri}")


async def main():
    """Main function to run the MCP server."""
    # Import here to avoid circular imports
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
