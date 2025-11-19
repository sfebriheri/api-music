from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json

from ...core.use_cases.music import MusicService
from ...infrastructure.external.youtube_repository import YouTubeRepository
from ...infrastructure.database.postgres_repository import PostgresRepository

app = Flask(__name__)

# Initialize services
music_repo = YouTubeRepository()
music_service = MusicService(music_repo)
db_repo = PostgresRepository()

# HTML Template (Simplified for brevity, same as before)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MCP Music API</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333; }
        .section { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        input { padding: 8px; margin-right: 10px; }
        pre { background: #f8f9fa; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 MCP Music API</h1>
        
        <div class="section">
            <h2>Search Music</h2>
            <input type="text" id="query" placeholder="Search query..." value="Radiohead">
            <select id="filter">
                <option value="songs">Songs</option>
                <option value="albums">Albums</option>
                <option value="artists">Artists</option>
            </select>
            <button onclick="search()">Search</button>
            <pre id="results"></pre>
        </div>
    </div>

    <script>
        async function search() {
            const query = document.getElementById('query').value;
            const filter = document.getElementById('filter').value;
            const res = await fetch(`/api/search?query=${encodeURIComponent(query)}&filter=${filter}`);
            const data = await res.json();
            document.getElementById('results').textContent = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search')
def search():
    try:
        query = request.args.get('query', '')
        filter_type = request.args.get('filter', 'songs')
        limit = int(request.args.get('limit', 10))
        results = music_service.search_music(query, limit, filter_type)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_app():
    app.run(host='0.0.0.0', port=5000, debug=True)
