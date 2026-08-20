# -*- coding: utf-8 -*-
"""
Agent Smith UI Branding and Theme Customizer
- Replaces VS Code icons in Titlebar and Welcome Tab with Agent Smith Brand SVG
- Replaces "Get Started with VS Code" -> "Get Started with Agent Smith"
- Replaces "Code - OSS" -> "Agent Smith"
"""

import os
import re
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def apply_branding(target_out_dir: Path):
    print("==================================================")
    print("[Agent Smith] Applying UI Branding & Icons...")
    print("==================================================")

    # 1. Read Brand SVG (docs/images/code-icon.svg)
    brand_svg_path = ROOT_DIR / "docs" / "images" / "code-icon.svg"
    if not brand_svg_path.exists():
        print(f"[!] Warning: Brand SVG not found at {brand_svg_path}")
        return

    with open(brand_svg_path, "r", encoding="utf-8") as f:
        brand_svg_raw = f.read()

    # URL-encode SVG for CSS data URI
    brand_svg_encoded = urllib.parse.quote(brand_svg_raw)
    brand_data_uri = f'data:image/svg+xml,{brand_svg_encoded}'

    # 2. Inject Brand SVG into workbench.desktop.main.css
    css_path = target_out_dir / "vs" / "workbench" / "workbench.desktop.main.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8", errors="ignore") as f:
            css_content = f.read()

        orig_css_len = len(css_content)

        # Replace all occurrences of default VS Code Layer_1 blue SVG data URI with brand SVG
        # Match data:image/svg+xml,%3Csvg id='Layer_1' ... %3C/svg%3E
        css_content = re.sub(
            r'data:image/svg\+xml,%3Csvg id=\'Layer_1\'[^\"]+',
            brand_data_uri,
            css_content
        )

        # Add explicit style overrides for titlebar window-appicon and welcome tab icon
        override_styles = f"""
/* --- Agent Smith Custom Brand Overrides --- */
.monaco-workbench .part.titlebar > .titlebar-container > .titlebar-left > .window-appicon:not(.codicon) {{
    background-image: url("{brand_data_uri}") !important;
    background-size: 18px 18px !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
}}
.show-file-icons .vscode_getting_started_page-name-file-icon.file-icon::before,
.show-file-icons .webview-vs_code_release_notes-name-file-icon.file-icon::before {{
    background-image: url("{brand_data_uri}") !important;
    background-size: 16px 16px !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
}}
"""
        if "Agent Smith Custom Brand Overrides" not in css_content:
            css_content += override_styles

        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        print(f"[ok] Injected brand logo into {css_path.name}")

    # 3. Replace Titles and Strings in workbench.desktop.main.nls.js
    nls_path = target_out_dir / "vs" / "workbench" / "workbench.desktop.main.nls.js"
    if nls_path.exists():
        with open(nls_path, "r", encoding="utf-8", errors="ignore") as f:
            nls_content = f.read()

        nls_content = nls_content.replace("Get Started with VS Code", "Get Started with Agent Smith")
        nls_content = nls_content.replace("Get Started with VS Code for the Web", "Get Started with Agent Smith for the Web")
        nls_content = nls_content.replace("Code - OSS", "Agent Smith")

        with open(nls_path, "w", encoding="utf-8") as f:
            f.write(nls_content)
        print(f"[ok] Updated welcome & branding strings in {nls_path.name}")

    # 4. Replace Titles and Strings in workbench.desktop.main.js
    wb_js_path = target_out_dir / "vs" / "workbench" / "workbench.desktop.main.js"
    if wb_js_path.exists():
        with open(wb_js_path, "r", encoding="utf-8", errors="ignore") as f:
            wb_js = f.read()

        wb_js = wb_js.replace("Get Started with VS Code", "Get Started with Agent Smith")
        wb_js = wb_js.replace("'Code - OSS Dev'", "'Agent Smith'")
        wb_js = wb_js.replace('"Code - OSS Dev"', '"Agent Smith"')
        wb_js = wb_js.replace("'Code - OSS'", "'Agent Smith'")
        wb_js = wb_js.replace('"Code - OSS"', '"Agent Smith"')

        with open(wb_js_path, "w", encoding="utf-8") as f:
            f.write(wb_js)
        print(f"[ok] Updated branding strings in {wb_js_path.name}")

    print("==================================================")
    print("[SUCCESS] UI Branding & Icon Customization Complete!")
    print("==================================================")

if __name__ == "__main__":
    out_dir = ROOT_DIR / "dist" / "agentsmith-desktop-v1.0.0" / "app" / "resources" / "app" / "out"
    if not out_dir.exists():
        out_dir = ROOT_DIR / "vscode" / "out-vscode"
    apply_branding(out_dir)
