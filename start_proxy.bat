 @echo off
REM Neopets Proxy Startup Script for Windows

echo 🚀 Starting Neopets Proxy...

REM Start mitmproxy with our addon (quiet mode)
mitmdump -s neoproxy_addon.py --listen-port 8080 --listen-host 127.0.0.1 --quiet