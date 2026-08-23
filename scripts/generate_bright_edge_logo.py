# -*- coding: utf-8 -*-
"""
Generate Bright Edge Trinity Air Logo Assets (PNG & ICO)
Creates high-contrast, glowing aerodynamic Möbius 3-blade Trinity wings with neon cyan, electric purple, and crisp white accents.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT_DIR = Path(__file__).resolve().parent.parent

def draw_bright_edge_trinity_air(size=512):
    # Create transparent RGBA canvas
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scale = size / 256.0
    
    def sc(val):
        return val * scale

    # Colors
    cyan_bright = (0, 229, 255, 255)
    cyan_glow = (0, 229, 255, 140)
    purple_bright = (179, 136, 255, 255)
    purple_glow = (179, 136, 255, 140)
    sky_bright = (0, 176, 255, 255)
    white_pure = (255, 255, 255, 255)
    core_dark = (11, 13, 20, 255)

    # 1. Subtle Background Aura / Outer Glow
    glow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    
    # Outer Trinity Triangle Loop (Glow Layer)
    outer_loop = [
        (sc(128), sc(22)),
        (sc(218), sc(160)),
        (sc(104), sc(226)),
        (sc(26), sc(122)),
        (sc(128), sc(22))
    ]
    glow_draw.line(outer_loop, fill=(0, 229, 255, 100), width=int(sc(18)), joint="curve")
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=sc(5)))
    img = Image.alpha_composite(img, glow_img)

    # 2. Draw 3 Aerodynamic Trinity Wings
    draw = ImageDraw.Draw(img)

    # Wing 1 (Left to Top Flow - Cyan)
    wing1_pts = [
        (sc(48), sc(184)),
        (sc(28), sc(136)),
        (sc(44), sc(68)),
        (sc(128), sc(28)),
        (sc(144), sc(58)),
        (sc(152), sc(94)),
        (sc(136), sc(126)),
        (sc(96), sc(172)),
        (sc(48), sc(184))
    ]
    draw.polygon(wing1_pts, fill=(0, 229, 255, 45), outline=cyan_bright, width=int(sc(9)))

    # Wing 2 (Top to Right Flow - Purple)
    wing2_pts = [
        (sc(128), sc(28)),
        (sc(188), sc(44)),
        (sc(234), sc(106)),
        (sc(208), sc(184)),
        (sc(176), sc(174)),
        (sc(144), sc(154)),
        (sc(130), sc(126)),
        (sc(120), sc(62)),
        (sc(128), sc(28))
    ]
    draw.polygon(wing2_pts, fill=(179, 136, 255, 45), outline=purple_bright, width=int(sc(9)))

    # Wing 3 (Bottom Flow - Sky/White)
    wing3_pts = [
        (sc(208), sc(184)),
        (sc(164), sc(232)),
        (sc(92), sc(232)),
        (sc(48), sc(184)),
        (sc(76), sc(164)),
        (sc(112), sc(152)),
        (sc(144), sc(158)),
        (sc(194), sc(176)),
        (sc(208), sc(184))
    ]
    draw.polygon(wing3_pts, fill=(0, 176, 255, 45), outline=sky_bright, width=int(sc(9)))

    # 3. Inner Möbius Sharp Edge Line Ribbons
    mobius_line1 = [(sc(128), sc(32)), (sc(148), sc(92)), (sc(118), sc(140)), (sc(48), sc(184))]
    mobius_line2 = [(sc(208), sc(184)), (sc(148), sc(172)), (sc(118), sc(140)), (sc(128), sc(32))]
    mobius_line3 = [(sc(48), sc(184)), (sc(112), sc(216)), (sc(168), sc(188)), (sc(208), sc(184))]
    
    draw.line(mobius_line1, fill=white_pure, width=int(sc(6)), joint="curve")
    draw.line(mobius_line2, fill=cyan_bright, width=int(sc(6)), joint="curve")
    draw.line(mobius_line3, fill=(234, 128, 252, 255), width=int(sc(6)), joint="curve")

    # 4. Central Air Vortex & Pulsar Energy Nodes
    def draw_node(cx, cy, r_outer, r_inner, color_outer, color_inner):
        draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=color_outer)
        draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], fill=color_inner)

    # Center Vortex Core
    draw.ellipse([sc(128) - sc(14), sc(142) - sc(14), sc(128) + sc(14), sc(142) + sc(14)], fill=core_dark, outline=cyan_bright, width=int(sc(6)))
    draw.ellipse([sc(128) - sc(5), sc(142) - sc(5), sc(128) + sc(5), sc(142) + sc(5)], fill=white_pure)

    # 3 Apex Nodes
    draw_node(sc(128), sc(28), sc(7), sc(3), white_pure, cyan_bright)
    draw_node(sc(48), sc(184), sc(7), sc(3), cyan_bright, white_pure)
    draw_node(sc(208), sc(184), sc(7), sc(3), purple_bright, white_pure)

    return img

def main():
    print("[*] Generating Bright Edge Trinity Air Logo assets...")
    
    # 1. 512x512 Master PNG
    master_img = draw_bright_edge_trinity_air(512)
    master_path = ROOT_DIR / "docs" / "images" / "logo.png"
    master_img.save(master_path, format="PNG")
    print(f"[ok] Saved Trinity Air master logo: {master_path}")

    # 2. 256x256 Code PNG
    code_img = draw_bright_edge_trinity_air(256)
    code_path = ROOT_DIR / "docs" / "images" / "code.png"
    code_img.save(code_path, format="PNG")
    print(f"[ok] Saved Trinity Air code logo: {code_path}")

    # 3. 64x64 Sidebar PNG for extension
    sidebar_img = draw_bright_edge_trinity_air(64)
    sidebar_dest = ROOT_DIR / "extension" / "agentsmith-chat" / "media" / "logo-sidebar.png"
    sidebar_dest.parent.mkdir(parents=True, exist_ok=True)
    sidebar_img.save(sidebar_dest, format="PNG")
    print(f"[ok] Saved Trinity Air sidebar logo: {sidebar_dest}")

    # 4. Multi-Resolution Windows ICO
    ico_path = ROOT_DIR / "docs" / "images" / "code.ico"
    master_img.save(
        ico_path, 
        format="ICO", 
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    )
    print(f"[ok] Saved Trinity Air multi-resolution icon: {ico_path}")

if __name__ == "__main__":
    main()
