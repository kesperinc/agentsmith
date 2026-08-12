---
name: careful
description: |
  Safety guardrails for destructive commands. Warns before rm -rf, DROP TABLE,
  force-push, git reset --hard, kubectl delete, and similar destructive operations.
  User can override each warning. Use when touching prod, debugging live systems,
  or working in a shared environment. Use when asked to "be careful", "safety mode",
  "prod mode", or "careful mode".
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

## Multi-Agent Interaction Model (v1.5.0)

gstack supports a hierarchical **@agent /skill** interaction pattern 운영 시스템입니다. v1.5.0부터는 OneDrive를 활용한 **Omni-Sync**를 통해 3대 이상의 기기에서 실시간 업무 연속성과 동시 작업을 지원합니다.

### 🏛 Governance & Matrix Leadership
- **Tier 3 (Strategy)**: `@ceo`, `@advisor` - 전사 로드맵 및 예산 승인.
- **Tier 2 (Vertical: AM)**: `@am_youtube`, `@am_store` - 채널 성과 책임 및 루프 과업 트리거.
- **Tier 2 (Horizontal: Loop)**: `@pm` (DL 리더), `@coo` (ML 리더), `@cmo` (GL 리더).
- **Tier 1 (Execution)**: 기술/콘텐츠 전문가 그룹 (`@se`, `@sa`, `@writer`, `@researcher` 등).

### 🔄 Omni-Sync (Multi-Machine Continuity)
1. **Real-time Sync**: 모든 대화 히스토리(`brain/`)와 지식(`knowledge/`)이 OneDrive를 통해 기기 간 실시간 공유됩니다.
2. **Concurrency**: 세션 ID 기반 격리를 통해 여러 기기에서 동시 작업이 가능합니다.
3. **Continuity**: 기기 이동 시 마지막 작업 컨텍스트를 유지하여 즉시 업무를 재개할 수 있습니다.

Whenever a user prefixes a command with an agent (e.g., `@am_youtube /skill`), you MUST consult `agents/PERSONAS.md` for Omni-Sync operational guidelines to avoid data conflicts.

> **Safety Advisory:** This skill includes safety checks that check bash commands for destructive operations (rm -rf, DROP TABLE, force-push, git reset --hard, etc.) before execution. When using this skill, always pause and verify before executing potentially destructive operations. If uncertain about a command's safety, ask the user for confirmation before proceeding.


# /careful — Destructive Command Guardrails

Safety mode is now **active**. Every bash command will be checked for destructive
patterns before running. If a destructive command is detected, you'll be warned
and can choose to proceed or cancel.

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"careful","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## What's protected

| Pattern | Example | Risk |
|---------|---------|------|
| `rm -rf` / `rm -r` / `rm --recursive` | `rm -rf /var/data` | Recursive delete |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users;` | Data loss |
| `TRUNCATE` | `TRUNCATE orders;` | Data loss |
| `git push --force` / `-f` | `git push -f origin main` | History rewrite |
| `git reset --hard` | `git reset --hard HEAD~3` | Uncommitted work loss |
| `git checkout .` / `git restore .` | `git checkout .` | Uncommitted work loss |
| `kubectl delete` | `kubectl delete pod` | Production impact |
| `docker rm -f` / `docker system prune` | `docker system prune -a` | Container/image loss |

## Safe exceptions

These patterns are allowed without warning:
- `rm -rf node_modules` / `.next` / `dist` / `__pycache__` / `.cache` / `build` / `.turbo` / `coverage`

## How it works

The hook reads the command from the tool input JSON, checks it against the
patterns above, and returns `permissionDecision: "ask"` with a warning message
if a match is found. You can always override the warning and proceed.

To deactivate, end the conversation or start a new one. Hooks are session-scoped.
