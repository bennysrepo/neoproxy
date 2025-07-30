 # 🎮 Neopets Flash Game Proxy

> **Fix broken Neopets Flash games without switching browsers**

A mitmproxy addon that intercepts and modifies Neopets game requests to restore functionality to broken Flash games. This project focuses on fixing game-breaking issues while maintaining the original gaming experience.

---

## 👨‍💻 About the Developer

**[Squirtle](https://clraik.com/forum/member.php?7889-Squirtle)** from [clraik.com](https://clraik.com) - Developer of various Neopets tools and utilities. This proxy helps restore functionality to games that have become unplayable due to Flash deprecation and server-side changes, allowing players to enjoy their favorite Neopets games without needing to switch browsers or use complex workarounds.

---

## 🎯 Fixed Games

| Game | Issue | Fix | Status |
|------|-------|-----|--------|
| Assignment 53 | Game wouldn't load at all | Game now loads and runs properly | Fully playable |
| Bubble Beams | Players would fall through the map | Collision system restored | Fully playable |
| Dubloon Disaster | Score submission was broken | Score sending now works correctly | Fully playable |
| Extreme Potato Counter | Game wouldn't load at all | Game now loads and runs properly | Fully playable |
| Ultimate Bullseye II | Arrows on the board weren't registering hits | Restored point system functionality | Fully playable |

---

## 🚧 Games Needing Fixes

| Game | Issue | Status |
|------|-------|--------|
| Clara on Ice | Fails to load the game | Needs investigation |
| Coal War Tactics | Labels fail to load, opponent never sets game up | Needs investigation |
| Cooty Wars | Shooting mootixs not being recognised | Needs investigation |
| Dueling Decks | Opponent never picks a category | Needs investigation |
| Extreme Herder | Petpets walk out of bounds | Needs investigation |
| Hotdog Hero | Broken collision detection | Needs investigation |
| Kreludan Mining Corp. | Broken controls, visuals, collision | Needs investigation |
| Let It Slide | Fails to load the game | Needs investigation |
| Moltara Run | Objects kill you before they should | Needs investigation |
| Neopian Battlefield Legends | Can't place towers on the map | Needs investigation |
| Pakiko | Failed to load the game | Needs investigation |
| Petpetsitter | Can't put petpets away | Needs investigation |
| Ready to Roll | Game mechanics are completely broken | Needs investigation |
| Shenkuu Tangram | Can't rotate puzzle pieces | Needs investigation |
| Tubular Kiko Racing | Map doesn't load | Needs investigation |
| Volcano Run II | Map positioning kills you sooner than it should | Needs investigation |
| Whirlpool | Impossible to beat levels | Needs investigation |
| Wingoball | Can't throw the ball | Needs investigation |
| Zurroball | Can't click on the balls, collision issue | Needs investigation |

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **pip** (usually comes with Python)
3. **A modern web browser** (Chrome, Firefox, Edge)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/neoproxy.git
cd neoproxy

# Install dependencies
pip install -r requirements.txt
```

### Setup

1. **Start the proxy** (choose your OS):

   **Windows:**
   ```cmd
   python start_proxy.py
   ```
   
   **macOS/Linux:**
   ```bash
   python start_proxy.py
   ```
   
   **Alternative (macOS/Linux only):**
   ```bash
   ./start_proxy.sh
   ```

2. **Generate mitmproxy certificate**:
   ```bash
   mitmdump --set confdir=~/.mitmproxy
   ```

3. **Install certificate in your browser**:
   - **Chrome**: Settings → Privacy and Security → Security → Manage Certificates → Import
   - **Firefox**: Settings → Privacy & Security → View Certificates → Import
   - **Edge**: Settings → Privacy, Search, and Services → Security → Manage Certificates → Import

4. **Configure proxy**:
   - **FoxyProxy** (Recommended): Install extension and add proxy with:
     - Host: `127.0.0.1`
     - Port: `8080`
   - **Manual**: Set system proxy to `127.0.0.1:8080`

---

## 🔧 Advanced Setup

### Using FoxyProxy (Recommended)

1. Install [FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/) extension
2. Add new proxy:
   ```
   Title: Neopets Proxy
   Proxy Type: HTTP
   IP Address: 127.0.0.1
   Port: 8080
   ```
3. Set URL pattern: `*neopets.com*`
4. Enable the proxy

### Manual Browser Configuration

#### Chrome/Edge
```bash
# Start Chrome with proxy
google-chrome --proxy-server="127.0.0.1:8080" --ignore-certificate-errors
```

#### Firefox
```bash
# Start Firefox with proxy
firefox --proxy-server="127.0.0.1:8080"
```

### System-Wide Proxy (All OS)

#### Windows
```cmd
# Set proxy via command line
netsh winhttp set proxy 127.0.0.1:8080
```

#### macOS
```bash
# Set proxy via command line
networksetup -setwebproxy "Wi-Fi" 127.0.0.1 8080
```

#### Linux
```bash
# Set proxy via environment variables
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
```

---

## 🎮 How It Works

The proxy uses advanced request interception to:

1. **Monitor game pages** and extract game names dynamically
2. **Cache play_flash requests** to prevent duplicate loading
3. **Inject modified SWF files** that fix game-breaking issues
4. **Rewrite URLs** to ensure proper resource loading
5. **Handle host redirections** for optimal performance

### Key Features

- **Dynamic Game Detection**: Automatically identifies games from page content
- **Smart Caching**: Prevents duplicate requests for better performance
- **SWF Injection**: Seamlessly replaces broken game files with fixed versions
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Browser Agnostic**: Compatible with all major browsers

---

## 📁 Project Structure

```
neoproxy/
├── neoproxy_addon.py    # Main proxy addon
├── start_proxy.py       # Cross-platform startup script
├── start_proxy.sh       # Unix startup script (alternative)
├── start_proxy.bat      # Windows startup script (alternative)
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── assets/
    └── swfs/           # Modified SWF files
        ├── ultimate_bullseye_ii/
        ├── dubloon_disaster/
        ├── assignment_53/
        └── bubble_beams/
```

---

## 🛠️ Development

### Adding New Game Fixes

1. **Identify the broken game** and its game ID
2. **Create modified SWF** that fixes the issue
3. **Place in appropriate directory**: `assets/swfs/{game_name}/`
4. **Test thoroughly** before releasing

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with multiple games
5. Submit a pull request

---

## ⚠️ Important Notes

- **This is NOT a cheating tool** - it only fixes broken games
- **Test thoroughly** - ensure fixes work across different scenarios

---

## 🆘 Troubleshooting

### Common Issues

**Certificate Errors**
```bash
# Regenerate certificate
rm -rf ~/.mitmproxy
mitmdump --set confdir=~/.mitmproxy
```

**Proxy Not Working**
- Check if port 8080 is available
- Ensure certificate is properly installed
- Verify proxy settings in browser

**Games Still Broken**
- Clear browser cache
- Restart the proxy
- Check if SWF files are in correct directories

---

## 📄 License

This project is provided as-is for educational and preservation purposes. Use at your own risk.

---

## 🙏 Acknowledgments

- **clraik.com community** for being amazing humans
- **mitmproxy team** for the excellent proxy framework