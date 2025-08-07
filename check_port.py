#!/usr/bin/env python3
"""
Port availability checker for the Expense Tracker
"""

import socket
import sys

def is_port_available(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8080, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return None

def main():
    """Main function to check port availability"""
    print("🔍 Checking port availability...")
    
    # Check common ports
    ports_to_check = [8080, 5000, 3000, 8000, 4000]
    
    for port in ports_to_check:
        if is_port_available(port):
            print(f"✅ Port {port} is available")
            return port
        else:
            print(f"❌ Port {port} is in use")
    
    # If none of the common ports are available, find any available port
    available_port = find_available_port(8080, 20)
    if available_port:
        print(f"✅ Found available port: {available_port}")
        return available_port
    else:
        print("❌ No available ports found in range 8080-8099")
        return None

if __name__ == "__main__":
    available_port = main()
    if available_port:
        print(f"\n💡 You can use port {available_port} for your application")
        print(f"   Update your configuration to use port {available_port}")
    else:
        print("\n❌ No available ports found. Please free up some ports and try again.")
        sys.exit(1) 