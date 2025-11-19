# MCP Music API

A Model Context Protocol (MCP) server example built with Python, featuring a **Clean Architecture** design. This project demonstrates how to create an MCP server with tools and resources using the official MCP Python library, with a focus on YouTube Music integration and PostgreSQL support.

## 🚀 Features

### Core Capabilities
- **Clean Architecture**: Organized into Core, Infrastructure, and Interface layers.
- **Dual Mode**: Runs as an MCP server (stdio) or a Web Interface (Flask).
- **Dependency Management**: Uses `uv` for fast and reliable package management.

### 🎵 YouTube Music Integration
- **Search**: Find songs, albums, artists, and playlists.
- **Details**: Get comprehensive metadata including lyrics, tracklists, and artist bios.
- **Downloads**: Download songs as MP3s with metadata.
- **Trending & Recommendations**: Discover new music.

### 🗄️ Database Support
- **PostgreSQL**: Full integration for querying and managing data.

## 📂 Project Structure

```
mcp-music-api/
├── src/
│   ├── core/
│   │   ├── entities/       # Data models (Song, Artist, Album)
│   │   └── use_cases/      # Business logic (MusicService)
│   ├── infrastructure/
│   │   ├── external/       # YouTubeRepository (ytmusicapi, pytube)
│   │   └── database/       # PostgresRepository
│   └── interfaces/
│       ├── mcp/            # MCP Server implementation
│       └── web/            # Flask Web App
├── main.py                 # Single entry point
└── requirements.txt
```

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.8+
- `uv` (recommended) or `pip`

### Running the Application

#### 1. 🌐 Web Interface (Recommended for Testing)
Start the Flask web interface to test features interactively.
```bash
uv run main.py web
# Open http://localhost:5000
```

#### 2. 📱 MCP Server (Stdio Mode)
Start the MCP server for integration with AI assistants (like Claude Desktop).
```bash
uv run main.py mcp
# OR just
uv run main.py
```

### Testing
Run the verification script to test core functionality:
```bash
uv run test_new_features.py
```

## 🔧 Available Tools

### YouTube Music Tools
- **youtube_search_music**: Search for music (songs, albums, artists, playlists).
- **youtube_get_song_details**: Get detailed song info including lyrics.
- **youtube_get_artist_details**: Get artist bio, top songs, and albums.
- **youtube_get_album_details**: Get album tracklist and metadata.
- **youtube_get_lyrics**: Get lyrics for a specific song.
- **youtube_download_mp3**: Download a song as MP3.
- **youtube_get_trending**: Get trending music.
- **youtube_get_recommendations**: Get music recommendations.
- **youtube_list_downloaded**: List downloaded MP3s.

### PostgreSQL Tools
- **postgres_query**: Execute SELECT queries.
- **postgres_execute**: Execute INSERT/UPDATE/DELETE commands.
- **postgres_list_tables**: List all tables.
- **postgres_get_schema**: Get table schema.

### Basic Tools
- **get_current_time**: Get current date and time.
- **calculate_sum**: Calculate sum of two numbers.
- **reverse_string**: Reverse a string.

## 📝 Configuration

### Environment Variables
Create a `.env` file to configure the database and download directory:

```bash
# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
# OR individual fields
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres

# YouTube Music
MUSIC_DOWNLOAD_DIR=~/Music/Downloads
```

## 📜 License
MIT
