---
name: freeze
description: |
  Restrict file edits to a specific directory for the session. Blocks Edit and
  Write outside the allowed path. Use when debugging to prevent accidentally
  "fixing" unrelated code, or when you want to scope changes to one module.
  Use when asked to "freeze", "restrict edits", "only edit this folder",
  or "lock down edits".
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

> **Safety Advisory:** This skill includes safety checks that verify file edits are within the allowed scope boundary before applying, and verify file writes are within the allowed scope boundary before applying. When using this skill, always pause and verify before executing potentially destructive operations. If uncertain about a command's safety, ask the user for confirmation before proceeding.


# /freeze — Restrict Edits to a Directory

Lock file edits to a specific directory. Any Edit or Write operation targeting
a file outside the allowed path will be **blocked** (not just warned).

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"freeze","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## Setup

Ask the user which directory to restrict edits to. Use AskUserQuestion:

- Question: "Which directory should I restrict edits to? Files outside this path will be blocked from editing."
- Text input (not multiple choice) — the user types a path.

Once the user provides a directory path:

1. Resolve it to an absolute path:
```bash
FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
echo "$FREEZE_DIR"
```

2. Ensure trailing slash and save to the freeze state file:
```bash
FREEZE_DIR="${FREEZE_DIR%/}/"
STATE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.gstack}"
mkdir -p "$STATE_DIR"
echo "$FREEZE_DIR" > "$STATE_DIR/freeze-dir.txt"
echo "Freeze boundary set: $FREEZE_DIR"
```

Tell the user: "Edits are now restricted to `<path>/`. Any Edit or Write
outside this directory will be blocked. To change the boundary, run `/freeze`
again. To remove it, run `/unfreeze` or end the session."

## How it works

The hook reads `file_path` from the Edit/Write tool input JSON, then checks
whether the path starts with the freeze directory. If not, it returns
`permissionDecision: "deny"` to block the operation.

The freeze boundary persists for the session via the state file. The hook
script reads it on every Edit/Write invocation.

## Notes

- The trailing `/` on the freeze directory prevents `/src` from matching `/src-old`
- Freeze applies to Edit and Write tools only — Read, Bash, Glob, Grep are unaffected
- This prevents accidental edits, not a security boundary — Bash commands like `sed` can still modify files outside the boundary
- To deactivate, run `/unfreeze` or end the conversation
