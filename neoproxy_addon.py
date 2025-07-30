#!/usr/bin/env python3

import re
from typing import Dict, Set, Optional

# Global state
game_pages: Set[str] = set()
game_names: Dict[str, str] = {}  # game_id -> game_name
blocked_requests: Set[str] = set()
response_cache: Dict[str, tuple[bytes, dict]] = {}  # URL -> (content, headers)



def load(loader):
    """Called when the addon is loaded."""
    print("🚀 Neopets Proxy Addon loaded")
    print("🔧 Addon is ready to intercept requests")
    print("📡 Waiting for Neopets traffic...")

def request(flow):
    """Intercept and process requests."""
    url = flow.request.url
    
    # Check if this is a Neopets game page
    if _is_neopets_game_page(url):
        game_id = _extract_game_id(url)
        if game_id:
            _handle_game_page_request(flow, game_id)
    
    # Check if this is a SWF file that we might want to replace
    elif _is_swf_request(url):
        _handle_swf_request(flow)
    
    # Check for duplicate play_flash requests and serve from cache
    elif _is_play_flash_request(url):
        _handle_play_flash_cache(flow)
    
    # Handle URL rewriting for SWF and config files
    elif _is_swf_or_config_request(url):
        _handle_url_rewrite(flow)
    
def response(flow):
    """Intercept and process responses."""
    # Cache play_flash responses for deduplication
    if _is_play_flash_request(flow.request.url):
        _cache_play_flash_response(flow)
    
    # Extract game names from game page HTML responses
    if _is_game_page_response(flow):
        _extract_game_name_from_response(flow)

def _is_neopets_game_page(url: str) -> bool:
    """Check if URL is a Neopets game page."""
    return (
        "neopets.com" in url and 
        "games/game.phtml" in url and 
        "game_id=" in url
    )

def _extract_game_id(url: str) -> Optional[str]:
    """Extract game ID from URL."""
    match = re.search(r'game_id=(\d+)', url)
    return match.group(1) if match else None

def _extract_game_name_from_html(html_content: str) -> Optional[str]:
    """Extract game name from HTML content."""
    # Pattern to match: <meta property="og:title" content="Games Room - Game Name"/>
    match = re.search(r'<meta property="og:title" content="Games Room - ([^"]+)"/>', html_content)
    if match:
        game_name = match.group(1).strip()
        # Convert to lowercase and replace spaces with underscores
        return game_name.lower().replace(' ', '_')
    return None

def _is_swf_request(url: str) -> bool:
    """Check if URL is a SWF file request."""
    return (
        "neopets.com" in url and
        ".swf" in url and
        re.search(r'g\d+_v\d+', url)  # Matches pattern like g772_v24
    )

def _extract_swf_info(url: str) -> Optional[tuple[str, str]]:
    """Extract game name and SWF filename from URL.
    Returns (game_name, swf_filename) or None if not found."""
    # Extract the SWF filename from the URL
    swf_match = re.search(r'/([^/]+\.swf)', url)
    if not swf_match:
        return None
    
    swf_filename = swf_match.group(1)
    
    # Extract game ID from SWF filename (e.g., g772_v24_14240.swf -> 772)
    game_id_match = re.search(r'g(\d+)_v', swf_filename)
    if not game_id_match:
        return None
    
    game_id = game_id_match.group(1)
    game_name = game_names.get(game_id, f"unknown_game_{game_id}")
    
    return (game_name, swf_filename)

def _is_play_flash_request(url: str) -> bool:
    """Check if URL is a play_flash request."""
    return (
        "neopets.com" in url and 
        ("play_flash.phtml" in url or "play_flash" in url)
    )

def _is_swf_or_config_request(url: str) -> bool:
    """Check if URL is a SWF or config file request that needs URL rewriting."""
    return (
        ".swf" in url or 
        "/config.xml" in url or 
        "/shellconfig.xml" in url
    )

def _handle_url_rewrite(flow) -> None:
    """Handle URL rewriting for SWF and config files."""
    url = flow.request.url
    
    # Rewrite host to images.neopets.com
    flow.request.host = "images.neopets.com"
    
    # Clean up URL path (remove duplicate /games/ segments)
    flow.request.url = re.sub(r"/games/.*/games/", "/games/", flow.request.url)
    flow.request.url = flow.request.url.replace("games/games", "games")
    
    # Force cache bypass by adding unique timestamp
    import time
    timestamp = int(time.time() * 1000)
    
    if "?" in flow.request.url:
        flow.request.url = f"{flow.request.url}&_nocache={timestamp}"
    else:
        flow.request.url = f"{flow.request.url}?_nocache={timestamp}"
    
    print(f"🔧 URL Rewritten: {url} -> {flow.request.url}")

def _handle_game_page_request(flow, game_id: str) -> None:
    """Handle requests to Neopets game pages."""
    # Only start monitoring if we haven't seen this game before
    if game_id not in game_pages:
        game_pages.add(game_id)
        print(f"🎮 Monitoring game ID: {game_id} (waiting for page load to get name)")
    else:
        game_name = game_names.get(game_id, f"unknown_game_{game_id}")
        print(f"🎮 Already monitoring {game_name} (ID: {game_id})")

def _handle_swf_request(flow) -> None:
    """Handle SWF file requests and replace with modified versions if available."""
    url = flow.request.url
    
    # Extract game name and SWF filename
    swf_info = _extract_swf_info(url)
    if not swf_info:
        return
    
    game_name, swf_filename = swf_info
    
    # Check if we have a modified version of this SWF
    modified_swf_path = f"assets/swfs/{game_name}/{swf_filename}"
    
    try:
        with open(modified_swf_path, 'rb') as f:
            modified_swf_data = f.read()
            
        # Create a response with our modified SWF
        from mitmproxy import http
        
        flow.response = http.Response.make(
            status_code=200,
            content=modified_swf_data,
            headers={
                "Content-Type": "application/x-shockwave-flash",
                "Content-Length": str(len(modified_swf_data)),
                "Cache-Control": "no-cache",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept, Origin, User-Agent",
                "Access-Control-Allow-Credentials": "true"
            }
        )
        
        print(f"🎯 SWF INJECTED: {game_name}/{swf_filename}")
        
    except FileNotFoundError:
        # No modified version available, let the original request proceed
        print(f"📁 No modified SWF found: {game_name}/{swf_filename}")
        pass
    except Exception as e:
        print(f"❌ Error loading modified SWF {game_name}/{swf_filename}: {e}")
        pass

def done():
    """Called when the addon is done."""
    print("🏁 Neopets Proxy Addon finished")
    
    # Log summary
    if game_pages:
        print(f"📊 Monitored games: {list(game_pages)}")
    
    if blocked_requests:
        print(f"📊 Blocked {len(blocked_requests)} requests") 

def _is_game_page_response(flow) -> bool:
    """Check if this is a game page HTML response."""
    return (
        "games/game.phtml" in flow.request.url and
        flow.response and
        "text/html" in flow.response.headers.get("content-type", "").lower()
    )

def _extract_game_name_from_response(flow) -> None:
    """Extract game name from game page HTML response."""
    try:
        content = flow.response.content.decode('utf-8', errors='ignore')
        game_id = _extract_game_id(flow.request.url)
        
        if game_id and game_id not in game_names:
            game_name = _extract_game_name_from_html(content)
            if game_name:
                game_names[game_id] = game_name
                print(f"🎯 Extracted game name: {game_name} (ID: {game_id})")
                # Update the monitoring message now that we have the name
                print(f"🎮 Now monitoring {game_name} (ID: {game_id})")
            else:
                print(f"⚠️  Could not extract game name for ID: {game_id}")
                
    except Exception as e:
        print(f"❌ Error extracting game name: {e}")

def _cache_play_flash_response(flow) -> None:
    """Cache play_flash responses for deduplication."""
    url = flow.request.url
    
    if flow.response and flow.response.status_code == 200:
        # Cache the response content and headers
        response_cache[url] = (
            flow.response.content,
            dict(flow.response.headers)
        )
        print(f"💾 Cached play_flash response for: {url[:100]}...")

def _handle_play_flash_cache(flow) -> None:
    """Handle play_flash requests with caching to prevent duplicates."""
    url = flow.request.url
    
    # Check if we have a cached response for this exact URL
    if url in response_cache:
        cached_content, cached_headers = response_cache[url]
        
        # Create response from cache
        from mitmproxy import http
        flow.response = http.Response.make(
            status_code=200,
            content=cached_content,
            headers=cached_headers
        )
        
        print(f"⚡ Served cached play_flash response for: {url[:100]}...")
        return
    
    # If not cached, let the request proceed normally
    # The response will be cached in the response handler
    print(f"📥 First play_flash request, will cache: {url[:100]}...")
