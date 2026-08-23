# -*- coding: utf-8 -*-
"""
Generate Bright Cybernetic Edge Agent Smith Logo (PNG & ICO)
Creates high-contrast, glowing edge lines with neon cyan/purple/white accents.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT_DIR = Path(__file__).resolve().parent.parent

def draw_bright_edge_logo(size=512):
    # Create transparent RGBA canvas
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    scale = size / 256.0
    
    def sc(val):
        return val * scale

    # Colors
    cyan_bright = (0, 240, 255, 255)
    cyan_mid = (0, 180, 255, 255)
    purple_bright = (190, 145, 255, 255)
    purple_deep = (140, 80, 255, 255)
    white_pure = (255, 255, 255, 255)
    lens_fill = (0, 229, 255, 60)

    # 1. Outer Cybernetic Hexagon Shield (Edge Line)
    hex_pts = [
        (sc(128), sc(16)),
        (sc(232), sc(74)),
        (sc(232), sc(182)),
        (sc(128), sc(240)),
        (sc(24), sc(182)),
        (sc(24), sc(74))
    ]
    
    # Outer Glow layer
    glow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.polygon(hex_pts, outline=(0, 229, 255, 120), width=int(sc(16)))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=sc(4)))
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img)

    # Hexagon crisp outer edge
    draw.polygon(hex_pts, outline=cyan_bright, width=int(sc(11)))

    # 2. Isometric Cube Edges
    # Top Face
    top_face = [
        (sc(128), sc(34)),
        (sc(212), sc(82)),
        (sc(128), sc(130)),
        (sc(44), sc(82))
    ]
    draw.polygon(top_face, outline=white_pure, width=int(sc(7)))

    # Left Face Edge
    left_edge = [
        (sc(44), sc(82)),
        (sc(44), sc(170)),
        (sc(128), sc(218))
    ]
    draw.line(left_edge, fill=cyan_bright, width=int(sc(7)), joint="curve")

    # Right Face Edge
    right_edge = [
        (sc(212), sc(82)),
        (sc(212), sc(170)),
        (sc(128), sc(218))
    ]
    draw.line(right_edge, fill=purple_bright, width=int(sc(7)), joint="curve")

    # Center Spindle
    draw.line([(sc(128), sc(130)), (sc(128), sc(218))], fill=white_pure, width=int(sc(7)))

    # 3. Agent Smith Cyber Sunglasses (Matrix Lens Edge Line)
    left_lens = [
        (sc(68), sc(116)),
        (sc(114), sc(116)),
        (sc(106), sc(146)),
        (sc(76), sc(146))
    ]
    right_lens = [
        (sc(142), sc(116)),
        (sc(188), sc(116)),
        (sc(180), sc(146)),
        (sc(150), sc(146))
    ]
    
    draw.polygon(left_lens, fill=lens_fill, outline=white_pure, width=int(sc(8)))
    draw.polygon(right_lens, fill=lens_fill, outline=white_pure, width=int(sc(8)))
    draw.line([(sc(114), sc(120)), (sc(142), sc(120))], fill=white_pure, width=int(sc(8)))

    # 4. Quantum Core Nodes
    def draw_glowing_circle(center, radius, color):
        cx, cy = center
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)

    draw_glowing_circle((sc(128), sc(74)), sc(9), white_pure)
    draw_glowing_circle((sc(86), sc(180)), sc(7), cyan_bright)
    draw_glowing_circle((sc(170), sc(180)), sc(7), purple_bright)

    # Accent Circuit Dashes
    draw.line([(sc(128), sc(74)), (sc(128), sc(108))], fill=white_pure, width=int(sc(4)))
    draw.line([(sc(86), sc(180)), (sc(128), sc(160))], fill=cyan_bright, width=int(sc(4)))
    draw.line([(sc(170), sc(180)), (sc(128), sc(160))], fill=purple_bright, width=int(sc(4)))

    return img

def main():
    print("[*] Generating Bright Edge Agent Smith Logo assets...")
    
    # 1. 512x512 Master PNG
    master_img = draw_bright_edge_logo(512)
    master_path = ROOT_DIR / "docs" / "images" / "logo.png"
    master_img.save(master_path, format="PNG")
    print(f"[ok] Saved master logo: {master_path}")

    # 2. 256x256 Code PNG
    code_img = draw_bright_edge_logo(256)
    code_path = ROOT_DIR / "docs" / "images" / "code.png"
    code_img.save(code_path, format="PNG")
    print(f"[ok] Saved code logo: {code_path}")

    # 3. 64x64 Sidebar PNG for extension
    sidebar_img = draw_bright_edge_logo(64)
    sidebar_dest = ROOT_DIR / "extension" / "agentsmith-chat" / "media" / "logo-sidebar.png"
    sidebar_dest.parent.mkdir(parents=True, exist_ok=True)
    sidebar_img.save(sidebar_dest, format="PNG")
    print(f"[ok] Saved sidebar logo: {sidebar_dest}")

    # 4. Multi-Resolution Windows ICO
    ico_path = ROOT_DIR / "docs" / "images" / "code.ico"
    master_img.save(
        ico_path, 
        format="ICO", 
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    )
    print(f"[ok] Saved multi-resolution icon: {ico_path}")

if __name__ == "__main__":
    main()
