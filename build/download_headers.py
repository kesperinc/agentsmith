import os
import urllib.request
import ssl
from pathlib import Path

# Base download paths
base_dir = Path("agentsmith/build/headers")
node_bin_dir = Path("agentsmith/build/node")

# Create directories
node_bin_dir.mkdir(parents=True, exist_ok=True)

# Files map (relative destination -> remote URL)
files = {
    # 1. Electron v27.2.3 Headers (for client compilation)
    "v27.2.3/node-v27.2.3-headers.tar.gz": "https://electronjs.org/headers/v27.2.3/node-v27.2.3-headers.tar.gz",
    "v27.2.3/SHASUMS256.txt": "https://electronjs.org/headers/v27.2.3/SHASUMS256.txt",
    "v27.2.3/win-x64/node.lib": "https://electronjs.org/headers/v27.2.3/win-x64/node.lib",
    
    # 2. Node.js v18.17.1 Headers (for remote components compilation)
    "v18.17.1/node-v18.17.1-headers.tar.gz": "https://nodejs.org/dist/v18.17.1/node-v18.17.1-headers.tar.gz",
    "v18.17.1/SHASUMS256.txt": "https://nodejs.org/dist/v18.17.1/SHASUMS256.txt",
    "v18.17.1/win-x64/node.lib": "https://nodejs.org/dist/v18.17.1/win-x64/node.lib"
}

# Disable SSL verification for downloader
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Download headers and config files
for rel_path, url in files.items():
    dest_file = base_dir / rel_path
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"[SCAN] Downloading: {url}")
    try:
        with urllib.request.urlopen(url, context=ctx) as response, open(dest_file, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[OK] Downloaded {rel_path} successfully.")
    except Exception as e:
        print(f"[FAIL] Download failed for {rel_path}: {e}")
        exit(1)

# 3. Download Portable Node.js v18.17.1 to bypass Node 24 spawn EINVAL errors
portable_node_url = "https://nodejs.org/dist/v18.17.1/win-x64/node.exe"
portable_node_dest = node_bin_dir / "node.exe"
print(f"[SCAN] Downloading Portable Node.js (v18.17.1) from: {portable_node_url}")
try:
    with urllib.request.urlopen(portable_node_url, context=ctx) as response, open(portable_node_dest, 'wb') as out_file:
        out_file.write(response.read())
    print("[OK] Portable Node.js v18.17.1 downloaded successfully.")
except Exception as e:
    print(f"[FAIL] Node.js download failed: {e}")
    exit(1)

print("[OK] All Electron and Node.js compilation assets (including Node v18) downloaded successfully.")
