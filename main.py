import sys
import asyncio
import argparse
from src.interfaces.mcp.server import run as run_mcp
from src.interfaces.web.app import run_app

def main():
    parser = argparse.ArgumentParser(description="MCP Music API Server")
    parser.add_argument('mode', choices=['mcp', 'web'], nargs='?', default='mcp', help="Run mode: 'mcp' (default) or 'web'")
    args = parser.parse_args()

    if args.mode == 'web':
        print("Starting Web Interface...")
        run_app()
    else:
        print("Starting MCP Server (stdio)...", file=sys.stderr)
        asyncio.run(run_mcp())

if __name__ == "__main__":
    main()
