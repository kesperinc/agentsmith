# 📋 2026-08-24 Agent Smith 아이콘 클릭 시 빈 창 버그 원인 규명 및 수정 명세서

**문서 일자**: 2026-08-24  
**버그 심각도**: Critical (기능 불가)  
**관련 파일**:
- `scripts/package_desktop_dist.py` (근본 원인 수정)
- `dist/agentsmith-desktop-v1.0.0/app/resources/app/extensions/agentsmith-chat/` (즉시 핫패치 적용)

---

## 1. 버그 증상

Agent Smith Desktop IDE 실행 후 좌측 액티비티 바의 **Agent Smith 아이콘 클릭 시 사이드바 패널에 아무 내용도 표시되지 않음**. (완전 빈 창)

---

## 2. 근본 원인 (Root Cause)

배포 스크립트(`scripts/package_desktop_dist.py` Line 306)에서 **잘못된 extension 소스 폴더**를 사용했습니다.

| 구분 | 소스 폴더 | `package.json` main | 상태 |
| :--- | :--- | :--- | :--- |
| **TypeScript 기반 (구버전)** | `extensions/agentsmith-chat/` | `"./out/extension.js"` | ❌ `out/` 폴더 미컴파일 → 활성화 실패 |
| **JS 기반 (최신 버전)** | `extension/agentsmith-chat/` | `"./src/extension.js"` | ✅ 즉시 실행 가능 |

배포 스크립트가 **TypeScript 기반 폴더(`extensions/`)** 의 `package.json`을 복사했고, 그 `main` 엔트리포인트가 `"./out/extension.js"` 이었지만 TypeScript 컴파일된 `out/` 폴더가 없어 확장이 활성화에 실패하여 **빈 창**이 나타났습니다.

---

## 3. 수정 내용 (Fix)

### ① 스크립트 근본 원인 수정 (`scripts/package_desktop_dist.py`, L305~L323)

```diff
-# 6.1 Copy Built-in Extension: extensions/agentsmith-chat
-EXTENSION_SRC = ROOT_DIR / "extensions" / "agentsmith-chat"
+# 6.1 Copy Built-in Extension: extension/agentsmith-chat (JS 기반 최신 버전 우선)
+# ※ extensions/(TypeScript 기반) 대신 extension/(순수 JS, main: ./src/extension.js) 를 사용합니다.
+EXTENSION_SRC = ROOT_DIR / "extension" / "agentsmith-chat"
+if not EXTENSION_SRC.exists():
+    EXTENSION_SRC = ROOT_DIR / "extensions" / "agentsmith-chat"
+...
+    # 기존에 잘못 복사된 TypeScript 버전 제거 후 정확한 JS 버전 복사
+    if EXTENSION_DEST1.exists():
+        shutil.rmtree(EXTENSION_DEST1, ignore_errors=True)
+    if EXTENSION_DEST2.exists():
+        shutil.rmtree(EXTENSION_DEST2, ignore_errors=True)
```

### ② 현재 배포 폴더 즉시 핫패치

- 배포된 `dist/agentsmith-desktop-v1.0.0/app/resources/app/extensions/agentsmith-chat/` 내의 TypeScript 기반 extension을 삭제하고 JS 기반 버전으로 즉시 교체
- `package.json` `main` 값: `./out/extension.js` → `./src/extension.js` 확인

---

## 4. 검증 결과

| 항목 | 교체 전 | 교체 후 |
| :--- | :--- | :--- |
| `package.json main` | `./out/extension.js` (없는 경로) | `./src/extension.js` ✅ |
| `src/extension.js` | 존재 (15,296 bytes) | 존재 (15,296 bytes) ✅ |
| `media/chat.html` | 존재 (4,231 bytes - 구버전) | 존재 (11,786 bytes - 최신) ✅ |
| `media/chat.js` | 존재 (10,436 bytes - 구버전) | 존재 (48,597 bytes - 최신) ✅ |
| `scripts/verify_desktop_bundle.py --verify-dist` | 통과 | 통과 ✅ |

> **예상 결과**: Agent Smith 아이콘 클릭 시 `extension.js`가 정상 로드되어 채팅 패널 UI가 표시됩니다.
