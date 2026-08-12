"""
VibeForge Secret Leak Prevention Checker
Checks for hardcoded OpenRouter / OpenAI / GCP API keys in source files before git commit.
"""

import sys
import re
from pathlib import Path

SECRET_PATTERNS = [
    (r'sk-or-v1-[a-zA-Z0-9]{32,}', "OpenRouter API Key"),
    (r'sk-[a-zA-Z0-9]{32,}', "OpenAI API Key"),
    (r'AIzaSy[a-zA-Z0-9_-]{33}', "GCP API Key"),
]

def scan_files():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    has_leak = False
    
    for file_path in base_dir.rglob("*"):
        if file_path.is_file() and not any(part in file_path.parts for part in ['.git', '.venv', '__pycache__', 'node_modules']):
            if file_path.suffix in ['.py', '.json', '.html', '.md', '.env']:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for pattern, secret_type in SECRET_PATTERNS:
                        if re.search(pattern, content):
                            # Ignore template files
                            if ".example" in file_path.name:
                                continue
                            print(f"❌ [SECRET LEAK WARNING] Found {secret_type} in: {file_path}")
                            has_leak = True
                except Exception:
                    pass
                    
    if has_leak:
        print("\n[BLOCKED] Git commit blocked due to secret leak hazard! Remove secret keys before committing.")
        sys.exit(1)
    else:
        print("[OK] Secret Checker: No secret leak hazards found. Safe to proceed.")
        sys.exit(0)

if __name__ == "__main__":
    scan_files()
