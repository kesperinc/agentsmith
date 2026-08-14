import os
from PIL import Image, ImageChops, ImageDraw

def rebuild():
    src_png = "docs/images/logo.png"
    if not os.path.exists(src_png):
        print(f"Error: logo.png not found at {src_png}")
        return

    print("Step 1: Analyzing original logo.png and side margins with threshold 45...")
    img = Image.open(src_png)
    rgb = img.convert("RGB")
    w, h = rgb.size
    
    # 0,0 픽셀 기준 배경색 감지
    bg_color = rgb.getpixel((0, 0))
    bg = Image.new("RGB", rgb.size, bg_color)
    diff = ImageChops.difference(rgb, bg)
    diff_gray = diff.convert("L")
    
    # 가장자리 50픽셀 영역의 노이즈 강제 제거 (테두리 오염 차단)
    draw = ImageDraw.Draw(diff_gray)
    draw.rectangle([0, 0, w, 50], fill=0)       # 상단
    draw.rectangle([0, h-50, w, h], fill=0)     # 하단
    draw.rectangle([0, 0, 50, h], fill=0)       # 좌측
    draw.rectangle([w-50, 0, w, h], fill=0)     # 우측
    
    # 임계값을 45로 상향 조정하여 눈에 안 보이는 미세 그림자/노이즈를 전면 차단
    # 이를 통해 육안으로 식별되는 진짜 글자/로고 본체만의 바운딩 박스를 검출
    diff_bin = diff_gray.point(lambda p: 255 if p > 45 else 0)
    bbox = diff_bin.getbbox()
    
    if not bbox:
        print("Warning: Content bounding box not found. Skipping.")
        return
        
    x_min, y_min, x_max, y_max = bbox
    print(f"-> Verified true content box: {bbox} on image size: {(w, h)}")
    
    # 각 사방의 진짜 원래 여백 크기 개별 계산
    left_orig = x_min
    right_orig = w - x_max
    top_orig = y_min
    bottom_orig = h - y_max
    print(f"-> Verified margins: Left={left_orig}px, Right={right_orig}px, Top={top_orig}px, Bottom={bottom_orig}px")
    
    # 각 방향별 원래 진짜 여백 크기의 정확히 25%만 잔류 (75%를 삭제하여 제거)
    left_new = int(left_orig * 0.25)       # 181 * 0.25 = 45px
    right_new = int(right_orig * 0.25)     # 183 * 0.25 = 45px
    top_new = int(top_orig * 0.25)         # 228 * 0.25 = 57px
    bottom_new = int(bottom_orig * 0.25)   # 228 * 0.25 = 57px
    
    # 좌측 여백 크기인 45px 만큼 우측도 똑같이 대칭 동조화 (이미 소수점 차이로 45px:45px로 동등하게 도출됨)
    print(f"-> Selected target margins (Symmetric): Left={left_new}px, Right={right_new}px, Top={top_new}px, Bottom={bottom_new}px")
    
    # 새로운 크롭 박스 범위 계산
    crop_box = (
        max(0, x_min - left_new),
        max(0, y_min - top_new),
        min(w, x_max + right_new),
        min(h, y_max + bottom_new)
    )
    print(f"-> New crop box coordinate: {crop_box}")
    
    # 원본 이미지에서 해당 크롭 박스로 물리적 크롭 후 저장
    cropped_img = img.crop(crop_box)
    cropped_img.save(src_png, format="PNG")
    print(f"Success: Cropped logo.png saved with size: {cropped_img.size}")

if __name__ == "__main__":
    rebuild()
