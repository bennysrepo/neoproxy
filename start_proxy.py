 #!/usr/bin/env python3
"""
Cross-platform Neopets Proxy Startup Script
Works on Windows, macOS, and Linux
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Neopets Proxy...")
    
    # Check if mitmproxy is installed
    try:
        subprocess.run(["mitmdump", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: mitmproxy not found. Please install it first:")
        print("   pip install mitmproxy")
        sys.exit(1)
    
    # Check if our addon exists
    if not os.path.exists("neoproxy_addon.py"):
        print("❌ Error: neoproxy_addon.py not found in current directory")
        sys.exit(1)
    
    # Start mitmproxy with our addon
    try:
        subprocess.run([
            "mitmdump", 
            "-s", "neoproxy_addon.py",
            "--listen-port", "8080",
            "--listen-host", "127.0.0.1",
            "--quiet"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Proxy stopped by user")
    except Exception as e:
        print(f"❌ Error starting proxy: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()