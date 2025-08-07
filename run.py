#!/usr/bin/env python3
"""
Expense Tracker Startup Script
Run this script to start the FastAPI backend server
"""

import os
import sys
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_port_availability(port=8080):
    """Check if the specified port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            print(f"✅ Port {port} is available")
            return True
    except OSError:
        print(f"❌ Port {port} is in use")
        return False

def find_available_port(start_port=8080, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Expense Tracker Server...")
    
    # Check port availability
    port = 8080
    if not check_port_availability(port):
        print(f"🔍 Looking for an available port...")
        available_port = find_available_port(8080, 20)
        if available_port:
            port = available_port
            print(f"✅ Found available port: {port}")
        else:
            print("❌ No available ports found. Please free up some ports and try again.")
            return False
    
    # Import and run the FastAPI app
    try:
        import sys
        backend_dir = Path(__file__).parent / "backend"
        sys.path.insert(0, str(backend_dir))
        from app import app
        import uvicorn
        
        print("✅ Server started successfully!")
        print(f"🌐 Backend API running at: http://localhost:{port}")
        print(f"📚 API Documentation available at: http://localhost:{port}/docs")
        print("📊 Frontend available at: frontend/index.html")
        print("📈 Analytics available at: frontend/charts.html")
        print("\n💡 Tips:")
        print("   - Open frontend/index.html in your browser")
        print("   - Or run: python -m http.server 8000 (from project root)")
        print("   - Then visit: http://localhost:8000/frontend/index.html")
        print(f"   - Check out the interactive API docs at: http://localhost:{port}/docs")
        print("\n🛑 Press Ctrl+C to stop the server")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open(f'http://localhost:{port}/docs')
            except:
                print(f"Could not open browser automatically. Please visit http://localhost:{port}/docs manually.")
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main function"""
    print("💰 Expense Tracker (FastAPI)")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start server
    if not start_server():
        sys.exit(1)

if __name__ == "__main__":
    main() 