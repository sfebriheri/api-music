#!/usr/bin/env python3
"""
Interactive Demo for MCP Server Functions

This script provides an interactive way to test individual functions
without needing the full MCP protocol.
"""

from youtube_music_service import youtube_music
from database_config import db_manager
from datetime import datetime

def demo_basic_functions():
    """Demo basic utility functions"""
    print("\n🔧 Basic Functions Demo")
    print("-" * 30)
    
    # Current time
    now = datetime.now()
    print(f"✅ Current time: {now.isoformat()}")
    
    # Math calculation
    a, b = 15, 7
    result = a + b
    print(f"✅ {a} + {b} = {result}")
    
    # String reverse
    text = "Hello World"
    reversed_text = text[::-1]
    print(f"✅ '{text}' reversed: '{reversed_text}'")

def demo_youtube_music():
    """Demo YouTube Music functionality"""
    print("\n🎵 YouTube Music Demo")
    print("-" * 30)
    
    try:
        # Search for music
        print("🔍 Searching for 'indie rock'...")
        results = youtube_music.search_music("indie rock", 3)
        
        if results and not results[0].get('error'):
            print(f"✅ Found {len(results)} songs:")
            for i, song in enumerate(results[:3], 1):
                print(f"   {i}. {song.get('title', 'Unknown')} by {song.get('artist', 'Unknown')}")
                print(f"      Duration: {song.get('duration', 'Unknown')}")
                print(f"      Video ID: {song.get('video_id', 'Unknown')}")
                print()
        else:
            print("❌ Search failed or no results")
            
        # Get trending music
        print("📈 Getting trending music...")
        trending = youtube_music.get_trending_music(3)
        
        if trending and not trending[0].get('error'):
            print(f"✅ Found {len(trending)} trending songs:")
            for i, song in enumerate(trending[:3], 1):
                print(f"   {i}. {song.get('title', 'Unknown')} by {song.get('artist', 'Unknown')}")
                print(f"      Rank: #{song.get('rank', 'Unknown')}")
                print()
        else:
            print("❌ Trending music failed or no results")
            
    except Exception as e:
        print(f"❌ YouTube Music demo failed: {e}")

def demo_database():
    """Demo database functionality"""
    print("\n🗄️ Database Demo")
    print("-" * 30)
    
    try:
        print(f"✅ Database URL: {db_manager.config.database_url}")
        print(f"✅ Host: {db_manager.config.host}")
        print(f"✅ Port: {db_manager.config.port}")
        print(f"✅ Database: {db_manager.config.database}")
        print(f"✅ User: {db_manager.config.user}")
        
        print("\n⚠️  Note: Database operations require a running PostgreSQL server")
        print("   To test database functions, start PostgreSQL and update .env file")
        
    except Exception as e:
        print(f"❌ Database demo failed: {e}")

def interactive_menu():
    """Interactive menu for testing functions"""
    while True:
        print("\n" + "=" * 50)
        print("🎯 MCP Server Interactive Demo")
        print("=" * 50)
        print("1. 🧪 Run All Demos")
        print("2. 🔧 Basic Functions")
        print("3. 🎵 YouTube Music")
        print("4. 🗄️ Database Config")
        print("5. 📱 Test MCP Server")
        print("6. 🚪 Exit")
        print("-" * 50)
        
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == "1":
            demo_basic_functions()
            demo_youtube_music()
            demo_database()
        elif choice == "2":
            demo_basic_functions()
        elif choice == "3":
            demo_youtube_music()
        elif choice == "4":
            demo_database()
        elif choice == "5":
            print("\n🚀 Starting MCP Server...")
            print("   (Press Ctrl+C to stop)")
            try:
                import subprocess
                subprocess.run(["python3", "mcp_server.py"])
            except KeyboardInterrupt:
                print("\n⏹️  MCP Server stopped")
            except Exception as e:
                print(f"❌ Failed to start MCP server: {e}")
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    print("🎉 Welcome to MCP Server Interactive Demo!")
    print("This demo will test all the functionality locally.")
    
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Check that all dependencies are installed:")
        print("   pip install -r requirements.txt")
