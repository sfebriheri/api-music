# 🚀 MCP Server Usage Guide

## 📋 Quick Start

Your MCP server is now **fully operational** with multiple testing options!

## 🎯 Testing Options

### **1. 🌐 Web Interface (Recommended for Testing)**
```bash
# Start the web demo
source venv/bin/activate
python3 web_demo.py

# Open your browser to: http://localhost:5000
```
**Features:**
- ✅ Interactive web interface
- ✅ Test all functions with buttons
- ✅ Real-time results display
- ✅ No command line needed

### **2. 🎮 Interactive Demo**
```bash
# Start interactive demo
source venv/bin/activate
python3 demo.py

# Choose from menu options 1-6
```
**Features:**
- ✅ Menu-driven interface
- ✅ Test individual functions
- ✅ Start MCP server from menu
- ✅ Easy to use

### **3. 🧪 Comprehensive Test Suite**
```bash
# Run full test suite
source venv/bin/activate
python3 test_server.py
```
**Features:**
- ✅ Tests all MCP server functions
- ✅ Tests services directly
- ✅ Detailed error reporting
- ✅ Protocol testing

### **4. 📱 MCP Server (Production Mode)**
```bash
# Start MCP server for client communication
source venv/bin/activate
python3 mcp_server.py
```
**Features:**
- ✅ Full MCP protocol support
- ✅ Ready for AI assistant integration
- ✅ Stdio communication mode

## 🎵 YouTube Music Features

### **Search Music:**
```bash
# Via demo script
python3 demo.py
# Choose option 3 (YouTube Music)

# Via web interface
# Go to http://localhost:5000
# Use the YouTube Music section
```

### **Download MP3:**
```bash
# The server supports MP3 downloads via MCP protocol
# Use an MCP client to call: youtube_download_mp3
```

### **Playlist Downloads:**
```bash
# Download entire playlists via MCP protocol
# Use an MCP client to call: youtube_download_playlist
```

## 🗄️ Database Features

### **Setup Database:**
1. Install PostgreSQL
2. Create `.env` file from `env_template.txt`
3. Update database credentials
4. Test connection via web interface

### **Database Operations:**
- ✅ Execute queries
- ✅ Insert/Update/Delete data
- ✅ List tables
- ✅ Get table schemas

## 🔧 Available Tools (15 Total)

### **Basic Tools (3):**
- `get_current_time` - Get current date/time
- `calculate_sum` - Add two numbers
- `reverse_string` - Reverse text

### **PostgreSQL Tools (4):**
- `postgres_query` - Execute SELECT queries
- `postgres_execute` - Execute INSERT/UPDATE/DELETE
- `postgres_list_tables` - List database tables
- `postgres_get_schema` - Get table schema

### **YouTube Music Tools (8):**
- `youtube_search_music` - Search for music
- `youtube_get_song_details` - Get song information
- `youtube_download_mp3` - Download MP3 files
- `youtube_download_playlist` - Download playlists
- `youtube_get_trending` - Get trending music
- `youtube_get_recommendations` - Get recommendations
- `youtube_list_downloaded` - List downloaded songs

## 🌟 Pro Tips

### **For Development:**
1. **Start with web interface** - Easy testing
2. **Use interactive demo** - Quick function testing
3. **Run test suite** - Comprehensive validation

### **For Production:**
1. **Use MCP server** - Full protocol support
2. **Set up database** - Enable all features
3. **Configure environment** - Customize settings

### **For AI Integration:**
1. **Start MCP server** - Ready for clients
2. **Use stdio mode** - Standard MCP communication
3. **Test with MCP client** - Verify integration

## 🚨 Troubleshooting

### **Common Issues:**
- **Import errors** → Check virtual environment activation
- **Database errors** → Verify PostgreSQL is running
- **YouTube errors** → Check internet connection
- **MCP server hanging** → Normal for stdio mode

### **Solutions:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python3 --version

# Verify virtual environment
which python3
```

## 🎉 Success Indicators

✅ **Web interface loads** → Flask working  
✅ **YouTube search works** → API integration working  
✅ **Database config loads** → Configuration working  
✅ **MCP server starts** → Protocol ready  
✅ **All tests pass** → System fully operational  

## 🔗 Next Steps

1. **Test web interface** - http://localhost:5000
2. **Try interactive demo** - `python3 demo.py`
3. **Run test suite** - `python3 test_server.py`
4. **Start MCP server** - `python3 mcp_server.py`
5. **Integrate with AI** - Use MCP client

---

**🎯 Your MCP server is ready for action!** 🚀
