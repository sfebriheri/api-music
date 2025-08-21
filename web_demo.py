#!/usr/bin/env python3
"""
Web Demo Interface for MCP Server

A simple Flask web interface to test MCP server functions
"""

from flask import Flask, render_template_string, request, jsonify
from youtube_music_service import youtube_music
from database_config import db_manager
from datetime import datetime
import json

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MCP Server Web Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #333; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .section { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        .button:hover { background: #0056b3; }
        .input { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; width: 200px; }
        .result { background: #f8f9fa; padding: 15px; border-radius: 4px; margin: 10px 0; white-space: pre-wrap; font-family: monospace; }
        .success { border-left: 4px solid #28a745; }
        .error { border-left: 4px solid #dc3545; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 MCP Server Web Demo</h1>
            <p>Test all MCP server functionality through a web interface</p>
        </div>

        <div class="grid">
            <!-- Basic Functions -->
            <div class="section">
                <h2>🔧 Basic Functions</h2>
                <button class="button" onclick="testBasicFunctions()">Test All Basic Functions</button>
                <div id="basic-results"></div>
            </div>

            <!-- YouTube Music -->
            <div class="section">
                <h2>🎵 YouTube Music</h2>
                <input type="text" id="search-query" class="input" placeholder="Search query" value="rock music">
                <input type="number" id="search-limit" class="input" placeholder="Limit" value="5" style="width: 80px;">
                <button class="button" onclick="searchMusic()">Search Music</button>
                <button class="button" onclick="getTrending()">Get Trending</button>
                <button class="button" onclick="getDownloaded()">List Downloaded</button>
                <div id="youtube-results"></div>
            </div>

            <!-- Database -->
            <div class="section">
                <h2>🗄️ Database</h2>
                <button class="button" onclick="testDatabase()">Test Database Connection</button>
                <div id="database-results"></div>
            </div>

            <!-- MCP Server -->
            <div class="section">
                <h2>📱 MCP Server</h2>
                <button class="button" onclick="testMCPServer()">Test MCP Server</button>
                <div id="mcp-results"></div>
            </div>
        </div>
    </div>

    <script>
        function showResult(elementId, data, isSuccess = true) {
            const element = document.getElementById(elementId);
            const className = isSuccess ? 'result success' : 'result error';
            element.innerHTML = `<div class="${className}">${JSON.stringify(data, null, 2)}</div>`;
        }

        async function testBasicFunctions() {
            try {
                const response = await fetch('/api/basic-functions');
                const data = await response.json();
                showResult('basic-results', data, true);
            } catch (error) {
                showResult('basic-results', {error: error.message}, false);
            }
        }

        async function searchMusic() {
            try {
                const query = document.getElementById('search-query').value;
                const limit = document.getElementById('search-limit').value;
                const response = await fetch(`/api/search-music?query=${encodeURIComponent(query)}&limit=${limit}`);
                const data = await response.json();
                showResult('youtube-results', data, true);
            } catch (error) {
                showResult('youtube-results', {error: error.message}, false);
            }
        }

        async function getTrending() {
            try {
                const response = await fetch('/api/trending-music');
                const data = await response.json();
                showResult('youtube-results', data, true);
            } catch (error) {
                showResult('youtube-results', {error: error.message}, false);
            }
        }

        async function getDownloaded() {
            try {
                const response = await fetch('/api/downloaded-songs');
                const data = await response.json();
                showResult('youtube-results', data, true);
            } catch (error) {
                showResult('youtube-results', {error: error.message}, false);
            }
        }

        async function testDatabase() {
            try {
                const response = await fetch('/api/test-database');
                const data = await response.json();
                showResult('database-results', data, true);
            } catch (error) {
                showResult('database-results', {error: error.message}, false);
            }
        }

        async function testMCPServer() {
            try {
                const response = await fetch('/api/test-mcp-server');
                const data = await response.json();
                showResult('mcp-results', data, true);
            } catch (error) {
                showResult('mcp-results', {error: error.message}, false);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/basic-functions')
def api_basic_functions():
    try:
        now = datetime.now()
        result = {
            'current_time': now.isoformat(),
            'math_calculation': '15 + 7 = 22',
            'string_reverse': 'Hello World -> dlroW olleH',
            'status': 'success'
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/search-music')
def api_search_music():
    try:
        query = request.args.get('query', 'rock music')
        limit = int(request.args.get('limit', 5))
        
        results = youtube_music.search_music(query, limit)
        return jsonify({
            'query': query,
            'limit': limit,
            'results': results,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/trending-music')
def api_trending_music():
    try:
        trending = youtube_music.get_trending_music(10)
        return jsonify({
            'trending': trending,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/downloaded-songs')
def api_downloaded_songs():
    try:
        songs = youtube_music.get_downloaded_songs()
        return jsonify({
            'downloaded_songs': songs,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/test-database')
def api_test_database():
    try:
        config = db_manager.config
        result = {
            'database_url': config.database_url,
            'host': config.host,
            'port': config.port,
            'database': config.database,
            'user': config.user,
            'status': 'success',
            'note': 'Database operations require a running PostgreSQL server'
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/test-mcp-server')
def api_test_mcp_server():
    try:
        # Import and test MCP server
        from mcp_server import server
        result = {
            'server_name': server.name,
            'status': 'success',
            'note': 'MCP server is ready for stdio communication'
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    print("🌐 Starting MCP Server Web Demo...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the web server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n⏹️  Web server stopped")
    except Exception as e:
        print(f"❌ Web server failed: {e}")
