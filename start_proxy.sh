#!/bin/bash

# Neopets Proxy Startup Script

echo "🚀 Starting Neopets Proxy..."

# Start mitmproxy with our addon (quiet mode)
mitmdump -s neoproxy_addon.py --listen-port 8080 --listen-host 127.0.0.1 --quiet 