# -*- coding: utf-8 -*-
import os
import json
import datetime

def update_version():
    # 현재 스크립트의 경로를 기준으로 vscode 디렉터리 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vscode_dir = os.path.join(current_dir, "..", "vscode")
    
    package_json_path = os.path.join(vscode_dir, "package.json")
    product_json_path = os.path.join(vscode_dir, "product.json")
    
    # 한국 표준시(KST) 기준으로 포맷된 현재 타임스탬프 생성
    tz_kst = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz_kst)
    timestamp = now.strftime("%Y%m%d.%H%M%S")
    
    # 1. package.json 업데이트
    if os.path.exists(package_json_path):
        with open(package_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        orig_version = data.get("version", "0.1.0")
        # 기존 버전에 이미 타임스탬프가 붙어있을 경우를 대비해 메이저/마이너/패치만 추출
        base_version = orig_version.split("-")[0]
        new_version = f"{base_version}-{timestamp}"
        
        data["version"] = new_version
        
        with open(package_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[성공] package.json 버전이 {new_version}으로 업데이트되었습니다.")
    else:
        print(f"[경고] package.json 파일을 찾을 수 없습니다: {package_json_path}")
        
    # 2. product.json 업데이트
    if os.path.exists(product_json_path):
        with open(product_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        orig_version = data.get("version", "0.1.0")
        base_version = orig_version.split("-")[0]
        new_version = f"{base_version}-{timestamp}"
        
        data["version"] = new_version
        
        with open(product_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[성공] product.json 버전이 {new_version}으로 업데이트되었습니다.")
    else:
        print(f"[경고] product.json 파일을 찾을 수 없습니다: {product_json_path}")

if __name__ == "__main__":
    update_version()
