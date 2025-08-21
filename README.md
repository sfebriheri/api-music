# MCP Testing Project (Python)

A Model Context Protocol (MCP) server example built with Python. This project demonstrates how to create an MCP server with tools and resources using the official MCP Python library.

## Features

### Tools
- **get_current_time**: Returns the current date and time
- **calculate_sum**: Calculates the sum of two numbers
- **reverse_string**: Reverses a given string
- **postgres_query**: Execute PostgreSQL SELECT queries
- **postgres_execute**: Execute PostgreSQL INSERT/UPDATE/DELETE commands
- **postgres_list_tables**: List all tables in the database
- **postgres_get_schema**: Get schema information for a specific table
- **youtube_search_music**: Search for music on YouTube Music
- **youtube_get_song_details**: Get detailed song information
- **youtube_download_mp3**: Download MP3 from YouTube Music
- **youtube_download_playlist**: Download entire playlists as MP3s
- **youtube_get_trending**: Get trending music from YouTube Music
- **youtube_get_recommendations**: Get music recommendations
- **youtube_list_downloaded**: List all downloaded MP3 songs

### Resources
- **example://system-info**: System information including database and YouTube Music status
- **example://sample-data**: Example data for testing purposes

## Prerequisites

- Python 3.8+
- pip or conda

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database connection (optional):
   - Create a `.env` file in the project root with your database credentials:
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```
   - Or configure your PostgreSQL connection directly in the code

4. Set up YouTube Music (optional):
   - No API key required for basic functionality
   - For advanced features, set environment variables:
   ```bash
   MUSIC_DOWNLOAD_DIR=/path/to/your/music/directory
   ```

5. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

### Development
```bash
python mcp_server.py
```

### Using with MCP Client
The server communicates via standard input/output, making it compatible with MCP clients.

## Project Structure

```
mcp-testing/
├── mcp_server.py         # Main MCP server implementation
├── database_config.py    # PostgreSQL database configuration
├── youtube_music_service.py # YouTube Music integration
├── requirements.txt      # Python dependencies
├── env_template.txt      # Database configuration template
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

## MCP Server Details

The server implements the following MCP capabilities:

- **Tool Calling**: Execute predefined functions using `@server.call_tool()` decorator
- **Resource Access**: Read data from predefined URIs using `@server.read_resource()` decorator
- **Stdio Transport**: Communicates via standard input/output using `stdio_server()`
- **PostgreSQL Integration**: Full database connectivity with query execution, schema inspection, and table management
- **YouTube Music Integration**: Search, browse, and download music from YouTube Music
- **MP3 Download**: Convert and download high-quality MP3 files from YouTube

## Example Tool Usage

### Get Current Time
```json
{
  "name": "get_current_time",
  "arguments": {}
}
```

### Calculate Sum
```json
{
  "name": "calculate_sum",
  "arguments": {
    "a": 5,
    "b": 3
  }
}
```

### Reverse String
```json
{
  "name": "reverse_string",
  "arguments": {
    "text": "Hello World"
  }
}
```

### PostgreSQL Query
```json
{
  "name": "postgres_query",
  "arguments": {
    "query": "SELECT * FROM users WHERE id = %s",
    "params": ["123"]
  }
}
```

### PostgreSQL Execute
```json
{
  "name": "postgres_execute",
  "arguments": {
    "command": "INSERT INTO users (name, email) VALUES (%s, %s)",
    "params": ["John Doe", "john@example.com"]
  }
}
```

### List Database Tables
```json
{
  "name": "postgres_list_tables",
  "arguments": {}
}
```

### Get Table Schema
```json
{
  "name": "postgres_get_schema",
  "arguments": {
    "table_name": "users"
  }
}
```

### YouTube Music Search
```json
{
  "name": "youtube_search_music",
  "arguments": {
    "query": "rock music",
    "limit": 5
  }
}
```

### Get Song Details
```json
{
  "name": "youtube_get_song_details",
  "arguments": {
    "video_id": "dQw4w9WgXcQ"
  }
}
```

### Download MP3
```json
{
  "name": "youtube_download_mp3",
  "arguments": {
    "video_id": "dQw4w9WgXcQ",
    "filename": "my_song.mp3"
  }
}
```

### Download Playlist
```json
{
  "name": "youtube_download_playlist",
  "arguments": {
    "playlist_id": "PLr8V2TxJRG0JzgM4..."
  }
}
```

### Get Trending Music
```json
{
  "name": "youtube_get_trending",
  "arguments": {
    "limit": 10
  }
}
```

### Get Music Recommendations
```json
{
  "name": "youtube_get_recommendations",
  "arguments": {
    "video_id": "dQw4w9WgXcQ",
    "limit": 5
  }
}
```

## Development

### Adding New Tools

1. Add the tool definition in the `list_tools()` function
2. Implement the tool logic in the `call_tool()` function
3. Add appropriate input validation using the `inputSchema`

### Adding New Resources

1. Add the resource definition in the `list_resources()` function
2. Implement the resource data in the `read_resource()` function
3. Specify appropriate MIME types

### Example Tool Implementation

```python
@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="my_new_tool",
            description="Description of my new tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description",
                    },
                },
                "required": ["param1"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "my_new_tool":
        param1 = arguments.get("param1", "")
        # Your tool logic here
        result = f"Processing {param1}"
        return [TextContent(type="text", text=result)]
```

## Dependencies

- `mcp>=1.0.0` - Official MCP Python library
- `psycopg2-binary>=2.9.0` - PostgreSQL database adapter
- `python-dotenv>=1.0.0` - Environment variable management
- `ytmusicapi>=1.7.0` - YouTube Music API integration
- `pytube>=15.0.0` - YouTube video downloading
- `requests>=2.31.0` - HTTP requests

## License

MIT

## YouTube Music Features

### 🎵 Music Discovery
- **Search**: Find songs, artists, and albums on YouTube Music
- **Trending**: Get trending music from YouTube Music charts
- **Recommendations**: Get music recommendations based on songs you like
- **Song Details**: Get comprehensive metadata including lyrics, duration, and more

### 📥 MP3 Downloads
- **Single Songs**: Download individual songs as MP3 files
- **Playlists**: Download entire playlists with one command
- **Custom Naming**: Specify custom filenames for downloads
- **Metadata**: Preserves song metadata in downloaded files

### 🔧 Technical Notes
- **No API Key Required**: Uses YouTube Music's public API
- **Download Directory**: Configurable via `MUSIC_DOWNLOAD_DIR` environment variable
- **Rate Limiting**: Respects YouTube's rate limits automatically
- **File Format**: Downloads as MP3 with proper metadata

### ⚠️ Important Notes
- **Terms of Service**: Ensure compliance with YouTube's Terms of Service
- **Copyright**: Only download content you have rights to
- **Quality**: Downloads audio in the best available quality
- **Speed**: Download speed depends on your internet connection

## Example Workflow

1. **Search for Music**:
   ```json
   {"name": "youtube_search_music", "arguments": {"query": "indie rock", "limit": 5}}
   ```

2. **Get Song Details**:
   ```json
   {"name": "youtube_get_song_details", "arguments": {"video_id": "VIDEO_ID"}}
   ```

3. **Download MP3**:
   ```json
   {"name": "youtube_download_mp3", "arguments": {"video_id": "VIDEO_ID"}}
   ```

4. **Download Entire Playlist**:
   ```json
   {"name": "youtube_download_playlist", "arguments": {"playlist_id": "PLAYLIST_ID"}}
   ```

## Contributing

Feel free to submit issues and pull requests to improve this MCP server example.
