# gstack 멀티 에이전트 실전 워크플로우 예제 (v1.2.0)

이 문서는 gstack의 Tier 기반 거버넌스와 Triple Loop 시스템을 활용한 실제 명령어 및 협업 시나리오를 제공합니다.

---

## 🔍 시나리오 1: 상향식 위기 대응 (Bottom-up RCA)
**상황**: 운영 모니터링 시스템에서 결제 성공률이 급감(Retention Down)하는 이벤트 감지.

1. **에이전트 투입 (RCA 분석)**
   > `@researcher /investigate "최근 1시간 내 결제 성공률 30% 급감 원인을 조사해줘"`
   - `@researcher`는 로그와 DB 상태를 분석하며, 감지된 [이벤트 로그 샘플](file:///c:/Users/kespe/OneDrive/antigravity/sunkim_gstack/examples/monitoring_events/ALARM_RETENTION_CRITICAL.json)을 활용하여 근본 원인을 파악하고 [RESEARCH_REPORT.md](file:///c:/Users/kespe/OneDrive/antigravity/sunkim_gstack/examples/reports/SAMPLE_PAYMENT_ISSUE_REPORT.md)를 작성합니다.

2. **리더 보고 및 대응 계획 (Escalation)**
   > `@devops "연구원의 보고서를 검토하고 긴급 패치 여부를 결정해줘"`
   - `@devops`는 인프라 리더로서 패치 범위를 확정하고 `@ceo`에게 보고합니다.

3. **최종 승인 및 실행**
   > `@ceo "비즈니스 손실 최소화를 위해 즉시 패치를 승인함. @se는 작업을 시작하세요."`
   - 이후 `@se /review` -> `@qa /qa` -> `@devops /ship` 순으로 루프가 회전합니다.

---

## 🎨 시나리오 2: 하향식 전략 변경 (Top-down Strategy)
**상황**: CEO가 현재 서비스의 성격이 '기능 중심'에서 '수익 중심'으로 전환되어야 함을 지시.

1. **전략 전파 (Strategic Directive)**
   > `@ceo /plan-ceo-review "현재 로드맵을 수익성(Margin) 극대화 관점에서 전면 재검토하세요."`

2. **루프 리더 백로그 설계**
   > `@pm "수익률 개선을 위한 성장 루프(GL) 가설 3가지를 도출하고 @growth와 협업하세요."`
   - `@pm`은 PM 리더로서 새로운 시장 테스트(GL) 일정을 수립합니다.

3. **아키텍처 대응**
   > `@sa "결제 및 유료 모델 아키텍처를 유연하게 확장할 수 있도록 설계를 보완하세요."`

---

## 🚀 시나리오 3: 고도화된 마케팅 오퍼레이션 (Marketing Ops)
**상황**: 신규 기능 출시에 맞춰 블로그 포스팅 및 SNS 홍보 캠페인 시작.

1. **팀 빌딩 및 전략 수립 (CMO 매니징)**
   > `@cmo "신규 기능 'AI 아키텍트' 론칭을 위한 순차적 마케팅 루프를 구성하고 @strategist에게 기획을 요청해줘"`
   - `@cmo`는 전체 일정을 관리하며 각 에이전트의 메모리 상태를 점검합니다.

2. **콘텐츠 생성 프로세스 (Sequential Process)**
   > `@writer "strategist의 기획안을 바탕으로 기술 블로그 초안(Markdown)을 작성하고 @editor에게 검수를 요청하세요."`
   - `@writer`가 초안을 작성하면 `@editor`가 SEO 최적화 및 톤앤매너를 검수합니다.

3. **최종 승인 및 발행**
   > `@editor "검수가 완료된 최종본을 @marketer에게 전달하여 발행 대기 상태로 만드세요."`
   - 이후 사람(User)의 최종 승인을 거쳐 외부 플랫폼에 배포됩니다.

---

## 📺 시나리오 4: YouTube AM의 채널 밀착형 대응 (Account Management)
**상황**: 유튜브 채널에서 제품에 대한 특정 불만 사항이 제기되고, 영상 조회수가 정체됨.

1. **이슈 탐지 및 전파 (AM Trigger)**
   > `@am_youtube "최근 영상 댓글에서 UX 관련 불만 정황을 포착했습니다. @researcher는 관련 댓글을 전수 분석하여 보고서를 작성하고, @pm에게 개선안 기획을 요청하세요."`
   - `@am_youtube`는 채널의 성과 파수꾼으로서 문제의 심각성을 정의하고 관련 전문가를 소환합니다.

2. **수평적 조직의 솔루션 도출**
   > `@pm "researcher의 보고서를 기반으로 UI 개선안을 확정했습니다. @se는 즉시 구현에 착수하고, @writer는 개편 소식을 알릴 커뮤니티 공지문을 작성하세요."`
   - 수평적 기술/마케팅 조직이 AM의 요청에 따라 각자의 전문성을 발휘합니다.

3. **최종 대응 및 효과 분석**
   > `@am_youtube "개선된 UI가 반영되었습니다. writer가 작성한 공지문을 유튜브 커뮤니티에 게시하고, 이후 시청자 반응 대시보드를 @analyst와 함께 분석하겠습니다."`
   - `@am_youtube`는 솔루션이 실제로 채널 유저들에게 어떻게 받아들여지는지 끝까지 책임집니다.

---

## 📊 시나리오 5: @researcher 상세 보고 예시
명령어: `@researcher /investigate Retention Down`

- **[공식 연구 보고서 템플릿]**(file:///c:/Users/kespe/OneDrive/antigravity/sunkim_gstack/examples/reports/RESEARCH_REPORT_TEMPLATE.md)
- **[Safari 브라우저 이슈 분석 보고서 샘플]**(file:///c:/Users/kespe/OneDrive/antigravity/sunkim_gstack/examples/reports/SAMPLE_PAYMENT_ISSUE_REPORT.md)
- **Executive Summary**: 모바일 Safari 환경에서의 결제 버튼 정렬 오류 발견.
- **Evidence**: `logs/prod-error.log` 내 JS ReferenceError 다수 발생.
- **Root Causes**: 최근 배포된 CSS 라이브러리 업데이트가 Safari 엔진과 충돌.
- **Strategic Recommendations**:
    - 즉시 롤백 대신 해당 CSS 모듈만 핫픽스 적용 권고.
    - 향후 `@qa` 루프에 Safari 교차 브라우저 테스트 케이스 강제화 제안.

---

## 💡 유용한 팁 (Best Practices)
- **명령어 결합**: `@pm /autoplan "무신사 스타일의 코디 추천 시스템 구축 팀을 꾸려줘"`와 같이 구체적으로 지시하세요.
- **권한 존중**: `@sa`에게 코드의 기술적 완성도를, `@pm`에게는 제품의 사용자 가치를 물어보는 것이 가장 효과적입니다.
- **보고서 요청**: 연구원 페르소나가 아니더라도 필요시 "보고서 형태로 정리해줘"라고 명시하면 아카이브가 용이합니다.
