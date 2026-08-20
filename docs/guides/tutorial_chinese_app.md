# gstack 실전 튜토리얼: 중국어 단어 맞추기 게임 만들기

이 튜토리얼은 `gstack` 에이전트 시스템을 사용하여 **"중국어 왕초보를 위한 병음/성조 분리 단어 맞추기 게임"**을 기획부터 배포 준비까지 어떻게 효율적으로 진행하는지 보여주는 실전 사례입니다.

---

## 🏗️ 기획부터 구현까지 (Phase Action Log)

### Phase 1: Planning (기획 및 PMF 검증)
- **사용 스킬:** `[/office-hours]`, `[/plan-ceo-review]`
- **결과물:**
  - 막연했던 "중국어 학습 서비스"를 **"병음 입력과 성조 선택을 2단계로 강제 분리하여 근육 기억(Muscle Memory)을 키우는 리듬 게임"**으로 구체화하고 다듬었습니다.
  - "복잡한 코드를 사용하는 화려한 앱" 대신 CEO 마인드에 기반하여 군더더기 학습 요소를 쳐내고 '단순 반복'에 집중했습니다.

### Phase 2: Design & Architecture (구조 설계)
- **사용 스킬:** `[/plan-eng-review]`, AI 코드 아키텍트와의 토론
- **결과물:**
  - **데이터베이스:** 백엔드 API와 서버 비용을 과감히 없애고, 프론트엔드에서 작동하는 `hsk_dictionary.js` 기반 정적(Static) 구조 채택.
  - **게이미피케이션 루프:** B2C 리텐션을 위해 출석 체크와 정답 코인을 획득하는 경제 로직(`economy.js`)을 설계하고 LocalStorage에 암호화하여 저장하기로 결정.

### Phase 3: Development (실전 개발)
- **사용 스킬:** `[/developer-guidelines]`, `[/design-system-rules]`
- **결과물:**
  - 지시받은 Karpathy 가이드라인에 맞춰 프레임워크(React, Vue) 없이 **가장 기초적인 바닐라 JavaScript 및 HTML/CSS**만을 사용하여 서버사이드 렌더링을 배제했습니다.
  - 최신 디자인 트렌드인 **Glassmorphism(글래스모피즘)** 속성(`backdrop-filter: blur()`)을 `design-system.css`에 구축하여 사용자에게 세련된 첫인상을 주었습니다.
  - `animations.css`를 통해 정답 시 코인이 쏟아져 내리는 파티클 이펙트와, 오답 시 화면이 흔들리는 `shake` 이펙트를 넣어 타격감을 극대화했습니다.

### Phase 4: QA & Release (검증 및 배포 준비)
- **사용 스킬:** `[/qa]`, `[/document-release]`
- **결과물:**
  - 브라우저에 의한 CORS 이슈(`file://` 규약에서 `fetch` 차단)를 조기에 발견하고, JSON을 전역 JS 객체로 마이그레이션하여 **로컬 서버 없이 더블 클릭만으로 완벽 구동**되도록 구조를 개선했습니다.
  - 사용자가 성공 이펙트를 기다리지 않고 버튼을 연타하여 발생하는 Race Condition 버그(하위 에러 출력 및 코인 무한 증식)를 찾아내어 UI State Lock(`isTransitioning`) 로직으로 방어했습니다.
  - 현재 코드는 오류 없이 동작하며, **언제든 정적 호스팅(GitHub Pages, Vercel 등) 플랫폼에 배포**할 수 있는 클린 상태입니다.

---

## 📂 파일 구조

생성된 파일들은 `examples/chinese_app/` 디렉토리 아래에 존재합니다.

```text
examples/chinese_app/
├── index.html                  # 메인 게임 스크립트 및 UI 마크업
├── js/
│   ├── core.js                 # 화면 제어 및 상태 머신 코어 루프
│   ├── render.js               # DOM 업데이트 및 애니메이션/사운드 로직
│   └── economy.js              # 코인, 출석, 반복 학습(LocalStorage) 제어
├── css/
│   ├── design-system.css       # 변수 및 Glassmorphism 레이아웃
│   └── animations.css          # 팝핑 효과 및 입자 이펙트 리소스
└── data/
    └── hsk_dictionary.js       # HSK 단어 사전 객체 DB (CORS 우회)
```

---

## 📝 결론
`gstack` 에이전트 워크플로우를 활용하면, 누구나 초기 아이디어가 **기획 ➡️ 아키텍처 수립 ➡️ 개발 ➡️ 버그 수정 ➡️ 산출물 문서화**의 모든 과정을 거쳐 단 몇 번의 채팅만으로 프로덕션 레벨의 모듈로 완성됩니다. 1인 솔로프레너(1인 기업가)로서 가장 효율적이고 강력한 무기를 갖게 된 것입니다.
