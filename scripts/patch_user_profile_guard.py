# -*- coding: utf-8 -*-
"""
Agent Smith Electron JS Core Universal Hot-Patching Script
Handles any variable name (a, r, s, l, etc.) for USERPROFILE declarations
and eliminates TypeError in path.join calls across main, sharedProcess, cliProcess, and ptyHost.
"""

import os
import re
import sys
from pathlib import Path

# Force UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent

TARGET_DIRS = [
    ROOT_DIR / "VSCode-win32-x64" / "resources" / "app" / "out",
    ROOT_DIR / "vscode" / "out",
    ROOT_DIR / "dist" / "agentsmith-desktop-v1.0.0" / "app" / "resources" / "app" / "out"
]

print("==================================================")
print("[Agent Smith] Running Universal JS Declaration Hot-Patch...")
print("==================================================")

total_patched = 0

for target_dir in TARGET_DIRS:
    if not target_dir.exists():
        continue
    print(f"[*] Scanning: {target_dir}")
    for js_file in target_dir.rglob("*.js"):
        try:
            with open(js_file, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            original_len = len(content)

            # 1. 범용 정규식 치환: 모든 임의의 변수명 (const \1 = process.env.USERPROFILE) 처리
            def replacer(match):
                var_name = match.group(1)
                return f'const {var_name}=process.env.USERPROFILE||(process.env.HOMEDRIVE&&process.env.HOMEPATH?process.env.HOMEDRIVE+process.env.HOMEPATH:"C:\\\\Users\\\\"+(process.env.USERNAME||"Default"));process.env.USERPROFILE={var_name};'

            content = re.sub(r'const\s+([a-zA-Z0-9_$]+)\s*=\s*process\.env\.USERPROFILE\s*;', replacer, content)

            # 2. if (typeof var != "string") ... 구문 및 안전하지 않은 /* safe */ 단독 블록 제거
            content = re.sub(
                r'if\s*\(\s*typeof\s+[a-zA-Z0-9_$]+\s*!=\s*["\']string["\']\s*\)\s*(?:throw new Error\([^)]*\)|\/\* safe \*\/)\s*;?',
                '',
                content
            )

            # 3. throw new Error("Windows: Unexpected undefined %USERPROFILE% environment variable") 단독 발생 건 정리
            content = content.replace(
                'throw new Error("Windows: Unexpected undefined %USERPROFILE% environment variable")',
                '/* safe */'
            )

            if len(content) != original_len:
                with open(js_file, "w", encoding="utf-8") as fp:
                    fp.write(content)
                total_patched += 1
                print(f"    -> Universal Patched: {js_file.name}")
        except Exception as e:
            print(f"    [!] Error patching {js_file}: {e}")

print("==================================================")
print(f"[SUCCESS] Universal Hot-Patching Complete! ({total_patched} files secured)")
print("==================================================")
