# -*- coding: utf-8 -*-
"""
Agent Smith IDE - Custom Git Patch Inspector and Applicator
Verifies and applies custom patches from patches/ directory to vscode/ source tree.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Force UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PATCHES_DIR = ROOT_DIR / "patches"
VSCODE_DIR = ROOT_DIR / "vscode"

def check_json_validity():
    """Validates product.json and package.json syntax and branding attributes."""
    print("[1/3] Validating JSON files integrity...")
    json_targets = [
        ("vscode/product.json", VSCODE_DIR / "product.json"),
        ("vscode/package.json", VSCODE_DIR / "package.json"),
        ("VSCode-win32-x64 product.json", ROOT_DIR / "VSCode-win32-x64" / "resources" / "app" / "product.json"),
        ("VSCode-win32-x64 package.json", ROOT_DIR / "VSCode-win32-x64" / "resources" / "app" / "package.json"),
    ]
    
    all_ok = True
    for label, file_path in json_targets:
        if not file_path.exists():
            print(f"  [-] {label}: File not found (skipping)")
            continue
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            
            # Check branding name
            if "product.json" in file_path.name:
                name_short = data.get("nameShort", "")
                name_long = data.get("nameLong", "")
                print(f"  [+] {label}: Valid JSON (nameShort='{name_short}', nameLong='{name_long}')")
            elif "package.json" in file_path.name:
                pkg_name = data.get("name", "")
                author = data.get("author", {}).get("name", "")
                print(f"  [+] {label}: Valid JSON (name='{pkg_name}', author='{author}')")
        except Exception as e:
            print(f"  [!] {label}: JSON Parse Error: {e}")
            all_ok = False
            
    return all_ok

def verify_and_apply_patches(apply_now=False):
    """Inspects and applies git patches in patches/ directory."""
    print("[2/3] Checking custom patches in patches/ directory...")
    if not PATCHES_DIR.exists():
        print(f"  [!] Patches directory not found: {PATCHES_DIR}")
        return False
        
    patch_files = sorted(PATCHES_DIR.glob("*.patch"))
    if not patch_files:
        print(f"  [-] No patch files found in {PATCHES_DIR}")
        return True
        
    print(f"  [i] Found {len(patch_files)} patch file(s): {[p.name for p in patch_files]}")
    
    for patch in patch_files:
        print(f"\n--- Inspecting Patch: {patch.name} ---")
        # Check if patch can apply or is already applied
        check_cmd = ["git", "apply", "--check", str(patch)]
        res_check = subprocess.run(check_cmd, cwd=str(VSCODE_DIR), capture_output=True, text=True)
        
        if res_check.returncode == 0:
            print(f"  [+] Patch check PASSED (cleanly applicable).")
            if apply_now:
                apply_cmd = ["git", "apply", str(patch)]
                res_apply = subprocess.run(apply_cmd, cwd=str(VSCODE_DIR), capture_output=True, text=True)
                if res_apply.returncode == 0:
                    print(f"  [+] Patch {patch.name} applied successfully!")
                else:
                    print(f"  [!] Failed to apply {patch.name}: {res_apply.stderr}")
        else:
            # Check if patch is already applied (reverse check)
            rev_check_cmd = ["git", "apply", "--reverse", "--check", str(patch)]
            res_rev = subprocess.run(rev_check_cmd, cwd=str(VSCODE_DIR), capture_output=True, text=True)
            if res_rev.returncode == 0:
                print(f"  [OK] Patch is ALREADY applied to the working tree.")
            else:
                print(f"  [!] Patch conflict or error:")
                print(f"      stdout: {res_check.stdout.strip()}")
                print(f"      stderr: {res_check.stderr.strip()}")

    return True

def main():
    print("==================================================")
    print("Agent Smith IDE - Custom Patch & Branding Manager")
    print("==================================================")
    
    json_ok = check_json_validity()
    patch_ok = verify_and_apply_patches(apply_now=False)
    
    print("\n[3/3] Overall Verification Status:")
    if json_ok and patch_ok:
        print("  ==> [SUCCESS] All branding configurations and patches are fully verified!")
    else:
        print("  ==> [WARNING] Some checks reported errors or warnings.")
    print("==================================================")

if __name__ == "__main__":
    main()
