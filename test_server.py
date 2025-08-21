#!/usr/bin/env python3
"""
Test Script for MCP Server

This script tests all the functionality of the MCP server locally
without needing an MCP client.
"""

import asyncio
import json
from mcp_server import server, list_tools, call_tool
from youtube_music_service import youtube_music
from database_config import db_manager

async def test_mcp_server():
    """Test all MCP server functionality"""
    
    print("🚀 Testing MCP Server Functionality")
    print("=" * 50)
    
    # Test 1: List all available tools
    print("\n1️⃣ Testing Tool Listing...")
    try:
        tools = await list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Tool listing failed: {e}")
    
    # Test 2: Test basic tools
    print("\n2️⃣ Testing Basic Tools...")
    
    # Test get_current_time
    try:
        result = await call_tool("get_current_time", {})
        print(f"✅ get_current_time: {result[0].text}")
    except Exception as e:
        print(f"❌ get_current_time failed: {e}")
    
    # Test calculate_sum
    try:
        result = await call_tool("calculate_sum", {"a": 5, "b": 3})
        print(f"✅ calculate_sum: {result[0].text}")
    except Exception as e:
        print(f"❌ calculate_sum failed: {e}")
    
    # Test reverse_string
    try:
        result = await call_tool("reverse_string", {"text": "Hello World"})
        print(f"✅ reverse_string: {result[0].text}")
    except Exception as e:
        print(f"❌ reverse_string failed: {e}")
    
    # Test 3: Test YouTube Music tools
    print("\n3️⃣ Testing YouTube Music Tools...")
    
    # Test music search
    try:
        result = await call_tool("youtube_search_music", {"query": "rock music", "limit": 3})
        print(f"✅ youtube_search_music: {result[0].text[:100]}...")
    except Exception as e:
        print(f"❌ youtube_search_music failed: {e}")
    
    # Test trending music
    try:
        result = await call_tool("youtube_get_trending", {"limit": 3})
        print(f"✅ youtube_get_trending: {result[0].text[:100]}...")
    except Exception as e:
        print(f"❌ youtube_get_trending failed: {e}")
    
    # Test 4: Test database tools
    print("\n4️⃣ Testing Database Tools...")
    
    # Test list tables (will fail if no database connection)
    try:
        result = await call_tool("postgres_list_tables", {})
        print(f"✅ postgres_list_tables: {result[0].text}")
    except Exception as e:
        print(f"❌ postgres_list_tables failed (expected if no DB): {e}")
    
    # Test 5: Test resources
    print("\n5️⃣ Testing Resources...")
    
    try:
        from mcp_server import list_resources, read_resource
        resources = await list_resources()
        print(f"✅ Found {len(resources)} resources:")
        for resource in resources:
            print(f"   - {resource['uri']}: {resource['name']}")
        
        # Test system info resource
        system_info = await read_resource("example://system-info")
        print(f"✅ system-info: {system_info[:200]}...")
        
    except Exception as e:
        print(f"❌ Resource testing failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 MCP Server Testing Complete!")

def test_youtube_service_directly():
    """Test YouTube Music service directly"""
    
    print("\n🎵 Testing YouTube Music Service Directly")
    print("=" * 50)
    
    try:
        # Test search
        print("\n1️⃣ Testing Music Search...")
        results = youtube_music.search_music("indie rock", 2)
        print(f"✅ Search results: {len(results)} songs found")
        for song in results[:2]:
            print(f"   - {song.get('title', 'Unknown')} by {song.get('artist', 'Unknown')}")
        
        # Test trending
        print("\n2️⃣ Testing Trending Music...")
        trending = youtube_music.get_trending_music(3)
        print(f"✅ Trending results: {len(trending)} songs found")
        for song in trending[:2]:
            print(f"   - {song.get('title', 'Unknown')} by {song.get('artist', 'Unknown')}")
        
        # Test downloaded songs
        print("\n3️⃣ Testing Downloaded Songs...")
        downloaded = youtube_music.get_downloaded_songs()
        print(f"✅ Downloaded songs: {len(downloaded)} found")
        if downloaded:
            for song in downloaded[:3]:
                print(f"   - {song.get('filename', 'Unknown')} ({song.get('size_mb', 0)} MB)")
        else:
            print("   - No songs downloaded yet")
            
    except Exception as e:
        print(f"❌ YouTube Music service test failed: {e}")

def test_database_service_directly():
    """Test database service directly"""
    
    print("\n🗄️ Testing Database Service Directly")
    print("=" * 50)
    
    try:
        print(f"✅ Database config loaded: {db_manager.config.database_url}")
        print(f"✅ Host: {db_manager.config.host}")
        print(f"✅ Port: {db_manager.config.port}")
        print(f"✅ Database: {db_manager.config.database}")
        print(f"✅ User: {db_manager.config.user}")
        
        # Note: Will fail if no actual database connection
        print("\n⚠️  Note: Database operations will fail without a running PostgreSQL server")
        
    except Exception as e:
        print(f"❌ Database service test failed: {e}")

if __name__ == "__main__":
    print("🧪 MCP Server Local Testing Suite")
    print("=" * 50)
    
    # Test services directly
    test_youtube_service_directly()
    test_database_service_directly()
    
    # Test MCP server functionality
    print("\n" + "=" * 50)
    print("🔄 Testing MCP Server Protocol Functions...")
    
    try:
        asyncio.run(test_mcp_server())
    except Exception as e:
        print(f"❌ MCP server testing failed: {e}")
        print("💡 This might be expected if the server has async issues")
    
    print("\n🎯 Testing Complete!")
    print("\n💡 To run the actual MCP server:")
    print("   python3 mcp_server.py")
    print("\n💡 To test individual functions:")
    print("   python3 test_server.py")
