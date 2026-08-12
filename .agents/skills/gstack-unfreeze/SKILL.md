---
name: unfreeze
description: |
  Clear the freeze boundary set by /freeze, allowing edits to all directories
  again. Use when you want to widen edit scope without ending the session.
  Use when asked to "unfreeze", "unlock edits", "remove freeze", or
  "allow all edits".
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


# /unfreeze — Clear Freeze Boundary

Remove the edit restriction set by `/freeze`, allowing edits to all directories.

```bash
mkdir -p ~/.gstack/analytics
echo '{"skill":"unfreeze","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

## Clear the boundary

```bash
STATE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.gstack}"
if [ -f "$STATE_DIR/freeze-dir.txt" ]; then
  PREV=$(cat "$STATE_DIR/freeze-dir.txt")
  rm -f "$STATE_DIR/freeze-dir.txt"
  echo "Freeze boundary cleared (was: $PREV). Edits are now allowed everywhere."
else
  echo "No freeze boundary was set."
fi
```

Tell the user the result. Note that `/freeze` hooks are still registered for the
session — they will just allow everything since no state file exists. To re-freeze,
run `/freeze` again.
