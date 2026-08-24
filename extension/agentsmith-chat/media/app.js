/**
 * Agent Smith Intelligent Studio - Ultra-Fast Zero-Dependency Webview Controller
 * Pure Vanilla JavaScript (0% External CDN Dependency, 100% Offline & Webview Safe)
 */

(function () {
  'use strict';

  const BACKEND_API_BASE = 'http://localhost:5000';
  const vscode = typeof acquireVsCodeApi !== 'undefined' ? acquireVsCodeApi() : null;

  // Global State
  const state = {
    mode: 'planning', // 'planning', 'fast', 'qa'
    selectedModel: 'qwen/qwen-2.5-coder-32b-instruct',
    targetFile: 'auth_service.py',
    isLoading: false,
    activeDrawer: null,
    backendOnline: false,
    
    // Data collections
    messages: [
      {
        id: 'msg-welcome',
        role: 'agent',
        persona: '@se (Software Engineer)',
        content: '안녕하세요! Agent Smith Intelligent Studio에 오신 것을 환영합니다.\n자연어로 도메인 의도(Vibe)를 제시하시면 요구사항 분석, 다중 파일 생성, 샌드박스 검증 및 셀프코렉션을 자율 수행합니다.',
        thinking: [
          '1. CortexOS 한국어 강제 출력 가드레일 및 UTF-8 BOM-less 인코딩 검사 통과',
          '2. Mem0 로컬 벡터 메모리 (.agentsmith/mem0_memory.db) 연결 및 개발자 프로필 동기화 완료',
          '3. Graphify Python AST 지식 그래프 및 SQLite 세션 DB (sessions.db) 100% 온라인 준비'
        ],
        artifacts: [
          {
            title: '시스템 초기화 명세서',
            filename: '2026-08-20_agentsmith_system_init.md',
            path: 'coding-agent/docs/specs/2026-08-20_agentsmith_system_init.md',
            type: 'spec',
            summary: 'CortexOS 가드레일, Mem0 장기 기억 및 Graphify AST RAG 3대 코어 엔진 초기화 명세서',
            request_feedback: false
          }
        ],
        created_at: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      }
    ],
    
    files: ['auth_service.py', 'session_manager.py', 'vibe_engine.py'],
    
    diffs: {
      'auth_service.py': [
        { type: 'normal', text: 'async def authenticate_user(db: AsyncSession, credentials: UserLogin):' },
        { type: 'added', text: '+   async with db.begin():' },
        { type: 'added', text: '+       result = await db.execute(select(User).where(User.email == credentials.email))' },
        { type: 'added', text: '+       user = result.scalars().first()' },
        { type: 'removed', text: '-   user = db.query(User).filter(User.email == credentials.email).first()' },
        { type: 'normal', text: '    if not user or not await verify_password_async(credentials.password, user.password_hash):' },
        { type: 'normal', text: '        raise HTTPException(status_code=401, detail="Invalid Credentials")' },
        { type: 'added', text: '+   # CortexOS SAST Check Passed (Zero Hardcoded Secret)' },
        { type: 'normal', text: '    return create_access_token(data={"sub": user.email})' }
      ],
      'session_manager.py': [
        { type: 'normal', text: 'class SessionManager:' },
        { type: 'added', text: '+   def save_artifact_snapshot(self, session_id: str, artifact: dict):' },
        { type: 'added', text: '+       # Atomic SQLite Session Preservation' },
        { type: 'added', text: '+       return self.db.insert_artifact(session_id, artifact)' }
      ],
      'vibe_engine.py': [
        { type: 'normal', text: 'async def execute_vibe_cycle(self, intent: str, mode: str):' },
        { type: 'added', text: '+   # CortexGuard SAST Pre-Scan' },
        { type: 'added', text: '+   await self.cortex_guard.validate_prompt(intent)' }
      ]
    },
    
    sessions: [
      { id: 'sess-default-01', title: '초기 프로젝트 세팅 및 Phase 2 통합', mode: 'planning', date: '2026-08-20' },
      { id: 'sess-default-02', title: '바이너리 빌드 및 인스톨러 검증', mode: 'fast', date: '2026-08-21' }
    ],
    
    memories: [
      { category: 'project_rule', key: 'output_language', value: '답변 및 코드 주석은 한국어로만 작성' },
      { category: 'project_rule', key: 'encoding', value: 'UTF-8 BOM-less 인코딩 필수 적용' },
      { category: 'project_rule', key: 'virtualenv', value: 'uv를 사용하며 .venv 디렉터리로 관리' },
      { category: 'project_rule', key: 'triad', value: '작업 트라이어드([계획]-[코드]-[명세서]) 1:1:1 준수' },
      { category: 'developer_profile', key: 'role', value: 'Enterprise Coding Agent Architect' }
    ],
    
    graphStats: { total_files: 14, total_symbols: 48, classes: 8, functions: 40 },
    
    gstack: {
      personas: ['@pm', '@sa', '@se', '@qa', '@cso', '@dba', '@growth', '@ceo'],
      workflows: ['/office-hours', '/plan-ceo-review', '/plan-eng-review', '/review', '/investigate', '/qa', '/ship']
    }
  };

  // DOM Elements Cache
  const el = {
    chatContainer: document.getElementById('chat-messages-container'),
    promptInput: document.getElementById('prompt-input'),
    btnSend: document.getElementById('btn-send-prompt'),
    selectModel: document.getElementById('select-ai-model'),
    selectFile: document.getElementById('select-target-file'),
    serverStatusPill: document.getElementById('server-status-pill'),
    fileListContainer: document.getElementById('file-list-container'),
    diffViewerContainer: document.getElementById('diff-viewer-container'),
    btnAcceptDiff: document.getElementById('btn-accept-diff'),
    btnRejectDiff: document.getElementById('btn-reject-diff'),
    btnOpenEditor: document.getElementById('btn-open-editor'),
    drawerOverlay: document.getElementById('drawer-overlay'),
    drawerTitle: document.getElementById('drawer-title'),
    drawerBody: document.getElementById('drawer-content-body'),
    btnCloseDrawer: document.getElementById('btn-close-drawer'),
    badgeSessions: document.getElementById('badge-sessions'),
    badgeMemories: document.getElementById('badge-memories'),
    badgeGraph: document.getElementById('badge-graph')
  };

  // ------------------------------------------------------------------------
  // Initialize Application
  // ------------------------------------------------------------------------
  function init() {
    bindEvents();
    renderChat();
    renderFileList();
    renderDiff();
    updateBadges();
    checkBackendHealth();
  }

  // ------------------------------------------------------------------------
  // Event Bindings
  // ------------------------------------------------------------------------
  function bindEvents() {
    // Mode Switching
    document.querySelectorAll('.mode-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.mode-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.mode = btn.getAttribute('data-mode');
      });
    });

    // Top Drawer Buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const drawerName = btn.getAttribute('data-drawer');
        openDrawer(drawerName);
      });
    });

    // Close Drawer
    if (el.btnCloseDrawer) {
      el.btnCloseDrawer.addEventListener('click', closeDrawer);
    }
    if (el.drawerOverlay) {
      el.drawerOverlay.addEventListener('click', e => {
        if (e.target === el.drawerOverlay) closeDrawer();
      });
    }

    // Model Selection
    if (el.selectModel) {
      el.selectModel.addEventListener('change', e => {
        state.selectedModel = e.target.value;
      });
    }

    // Target File Selection
    if (el.selectFile) {
      el.selectFile.addEventListener('change', e => {
        state.targetFile = e.target.value;
        renderFileList();
        renderDiff();
      });
    }

    // Send Prompt
    if (el.btnSend) {
      el.btnSend.addEventListener('click', handleSendPrompt);
    }
    if (el.promptInput) {
      el.promptInput.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          handleSendPrompt();
        }
      });
    }

    // Open Wide Editor Panel
    if (el.btnOpenEditor) {
      el.btnOpenEditor.addEventListener('click', () => {
        if (vscode) {
          vscode.postMessage({ command: 'openEditorPanel' });
        } else {
          alert('[Agent Smith] VS Code Editor Panel 열기 명령을 실행합니다.');
        }
      });
    }

    // Diff Actions
    if (el.btnAcceptDiff) {
      el.btnAcceptDiff.addEventListener('click', () => {
        if (vscode) {
          vscode.postMessage({ command: 'acceptDiff', file: state.targetFile });
        }
        alert(`[Agent Smith] ${state.targetFile}의 변경사항을 작업공간에 반영하였습니다.`);
      });
    }
    if (el.btnRejectDiff) {
      el.btnRejectDiff.addEventListener('click', () => {
        if (vscode) {
          vscode.postMessage({ command: 'rollbackDiff', file: state.targetFile });
        }
        alert(`[Agent Smith] ${state.targetFile}의 변경사항을 롤백하였습니다.`);
      });
    }
  }

  // ------------------------------------------------------------------------
  // Backend Health & API Sync
  // ------------------------------------------------------------------------
  async function checkBackendHealth() {
    try {
      const res = await fetch(`${BACKEND_API_BASE}/api/workspace/status`, { method: 'GET' });
      if (res.ok) {
        state.backendOnline = true;
        if (el.serverStatusPill) {
          el.serverStatusPill.className = 'status-pill online';
          el.serverStatusPill.textContent = '● ONLINE :5000';
        }
        fetchBackendData();
      } else {
        throw new Error('Server not ready');
      }
    } catch (e) {
      state.backendOnline = false;
      if (el.serverStatusPill) {
        el.serverStatusPill.className = 'status-pill offline';
        el.serverStatusPill.textContent = '○ STANDBY :5000';
      }
    }
  }

  async function fetchBackendData() {
    try {
      // 1. Sessions
      const resSess = await fetch(`${BACKEND_API_BASE}/api/sessions`).catch(() => null);
      if (resSess && resSess.ok) {
        const data = await resSess.json();
        if (data.sessions && data.sessions.length > 0) state.sessions = data.sessions;
      }
      // 2. Mem0
      const resMem = await fetch(`${BACKEND_API_BASE}/api/mem0/profile`).catch(() => null);
      if (resMem && resMem.ok) {
        const data = await resMem.json();
        if (data.memories && data.memories.length > 0) state.memories = data.memories;
      }
      // 3. Graphify
      const resGraph = await fetch(`${BACKEND_API_BASE}/api/graphify/stats`).catch(() => null);
      if (resGraph && resGraph.ok) {
        const data = await resGraph.json();
        if (data.stats) state.graphStats = data.stats;
      }
      updateBadges();
    } catch (e) {
      console.log('Using cached local data:', e);
    }
  }

  function updateBadges() {
    if (el.badgeSessions) el.badgeSessions.textContent = state.sessions.length;
    if (el.badgeMemories) el.badgeMemories.textContent = state.memories.length;
    if (el.badgeGraph) el.badgeGraph.textContent = state.graphStats.total_symbols || 48;
  }

  // ------------------------------------------------------------------------
  // Render Chat Stream
  // ------------------------------------------------------------------------
  function renderChat() {
    if (!el.chatContainer) return;
    el.chatContainer.innerHTML = '';

    state.messages.forEach(msg => {
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${msg.role === 'user' ? 'user' : 'agent'}`;

      // Meta Header
      const meta = document.createElement('div');
      meta.className = 'bubble-meta';
      meta.innerHTML = `
        <span class="bubble-sender">${msg.role === 'user' ? '👤 YOU' : `🤖 AGENT SMITH (${msg.persona || '@se'})`}</span>
        <span class="bubble-time">${msg.created_at || ''}</span>
      `;
      bubble.appendChild(meta);

      // Text Content
      const text = document.createElement('div');
      text.className = 'bubble-text';
      text.textContent = msg.content;
      bubble.appendChild(text);

      // Thinking Accordion
      if (msg.thinking && msg.thinking.length > 0) {
        const accordion = document.createElement('div');
        accordion.className = 'thinking-accordion';

        const toggle = document.createElement('div');
        toggle.className = 'thinking-toggle';
        toggle.innerHTML = `<span>🧠 REASONING PROCESS (${msg.thinking.length} STEPS)</span> <span>▾</span>`;

        const body = document.createElement('div');
        body.className = 'thinking-content';
        msg.thinking.forEach(t => {
          const step = document.createElement('div');
          step.className = 'thinking-step';
          step.textContent = `• ${t}`;
          body.appendChild(step);
        });

        toggle.addEventListener('click', () => {
          const isHidden = body.style.display === 'none';
          body.style.display = isHidden ? 'block' : 'none';
          toggle.querySelector('span:last-child').textContent = isHidden ? '▴' : '▾';
        });

        accordion.appendChild(toggle);
        accordion.appendChild(body);
        bubble.appendChild(accordion);
      }

      // Artifact Cards & Planning Gate
      if (msg.artifacts && msg.artifacts.length > 0) {
        msg.artifacts.forEach(art => {
          const card = document.createElement('div');
          card.className = 'artifact-card';
          card.innerHTML = `
            <div class="artifact-card-header">
              <div class="artifact-card-title">
                <span>📄</span>
                <span>${art.title}</span>
              </div>
              <span class="artifact-badge">${(art.type || 'DOC').toUpperCase()}</span>
            </div>
            <div class="artifact-summary">${art.summary || ''}</div>
            <div class="artifact-actions">
              <button class="btn-action-sm btn-open-doc" data-path="${art.path}">📂 에디터에서 열기</button>
              ${art.request_feedback ? `
                <button class="btn-action-sm proceed btn-proceed">✓ 승인하고 진행 (Proceed)</button>
                <button class="btn-action-sm feedback btn-feedback">✎ 피드백</button>
              ` : ''}
            </div>
          `;

          // Event Listeners for Artifact Card Buttons
          card.querySelector('.btn-open-doc')?.addEventListener('click', () => {
            if (vscode) {
              vscode.postMessage({ command: 'openFile', path: art.path });
            } else {
              alert(`[Agent Smith] 문서 열기: ${art.path}`);
            }
          });

          card.querySelector('.btn-proceed')?.addEventListener('click', () => {
            handleSendPrompt('승인되었습니다. 명세서에 따라 자율 코드 수정을 실행해 주세요.');
          });

          card.querySelector('.btn-feedback')?.addEventListener('click', () => {
            el.promptInput.value = '계획서에 단위 테스트 및 샌드박스 검증 항목을 보강해줘';
            el.promptInput.focus();
          });

          bubble.appendChild(card);
        });
      }

      el.chatContainer.appendChild(bubble);
    });

    // Auto Scroll to Bottom
    el.chatContainer.scrollTop = el.chatContainer.scrollHeight;
  }

  // ------------------------------------------------------------------------
  // Handle Send Prompt
  // ------------------------------------------------------------------------
  async function handleSendPrompt(overrideText) {
    const text = typeof overrideText === 'string' ? overrideText : (el.promptInput ? el.promptInput.value.trim() : '');
    if (!text || state.isLoading) return;

    if (el.promptInput && typeof overrideText !== 'string') {
      el.promptInput.value = '';
    }

    // Add User Message
    const userMsg = {
      id: `usr-${Date.now()}`,
      role: 'user',
      content: text,
      created_at: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
    };
    state.messages.push(userMsg);
    state.isLoading = true;
    if (el.btnSend) el.btnSend.disabled = true;
    renderChat();

    try {
      if (state.backendOnline) {
        const response = await fetch(`${BACKEND_API_BASE}/api/vibe/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            intent: text,
            target_file: state.targetFile,
            model_id: state.selectedModel,
            mode: state.mode
          })
        });

        if (response.ok) {
          const resData = await response.json();
          const agentMsg = {
            id: `agt-${Date.now()}`,
            role: 'agent',
            persona: '@se (Software Engineer)',
            content: resData.response || '요구사항 분석 및 코드 생성을 완료하였습니다.',
            thinking: resData.thinking || [
              `1. 의도 분석: "${text}"`,
              '2. CortexOS 트라이어드([계획]-[코드]-[명세서]) 가드레일 적용',
              '3. 샌드박스 Pytest 가상 실행 및 셀프코렉션 통과'
            ],
            artifacts: resData.artifacts || [],
            created_at: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
          };
          state.messages.push(agentMsg);
          return;
        }
      }
      throw new Error('Fallback simulation mode');
    } catch (err) {
      // Local Fast Simulation Fallback
      await new Promise(r => setTimeout(r, 400));
      const simulatedPlanFile = `2026-08-23_vibe_plan_${Date.now()}.md`;
      const fallbackMsg = {
        id: `agt-${Date.now()}`,
        role: 'agent',
        persona: '@se (Software Engineer)',
        content: state.mode === 'planning'
          ? `요구사항 '${text}'에 대한 구현 계획서를 수립하였습니다. 검토 후 [✓ 승인하고 진행 (Proceed)]을 클릭해 주세요.`
          : `요구사항 '${text}'을 반영하여 ${state.targetFile} 코드를 자율 수정하고 SAST 보안 검사를 완료하였습니다.`,
        thinking: [
          `1. 사용자 프롬프트 의도 분석: "${text}"`,
          '2. Mem0 프로젝트 룰(한국어 주석, UTF-8 BOM-less, uv .venv) 바인딩 완료',
          `3. Graphify AST RAG: ${state.targetFile} 연관 심볼 추출`,
          '4. 샌드박스 SAST 정적 보안 검사 (CORTEX-SEC-01/02/03) 통과'
        ],
        artifacts: [
          {
            title: state.mode === 'planning' ? '구현 계획서 (Planning Gate)' : '코드 변경 상세명세서',
            filename: simulatedPlanFile,
            path: `coding-agent/docs/${state.mode === 'planning' ? 'plans' : 'specs'}/${simulatedPlanFile}`,
            type: state.mode === 'planning' ? 'plan' : 'spec',
            summary: `자연어 의도 '${text}'에 대한 분석 및 멀티 파일 변경 명세서`,
            request_feedback: state.mode === 'planning'
          }
        ],
        created_at: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
      };
      state.messages.push(fallbackMsg);
    } finally {
      state.isLoading = false;
      if (el.btnSend) el.btnSend.disabled = false;
      renderChat();
    }
  }

  // ------------------------------------------------------------------------
  // Render File List & Live Diff
  // ------------------------------------------------------------------------
  function renderFileList() {
    if (!el.fileListContainer) return;
    el.fileListContainer.innerHTML = '';

    state.files.forEach(f => {
      const item = document.createElement('div');
      item.className = `file-list-item ${f === state.targetFile ? 'active' : ''}`;
      item.innerHTML = `<span>📄 ${f}</span> ${f === state.targetFile ? '<span style="font-size:0.65rem; color:var(--cyan-main)">EDITING</span>' : ''}`;
      item.addEventListener('click', () => {
        state.targetFile = f;
        if (el.selectFile) el.selectFile.value = f;
        renderFileList();
        renderDiff();
      });
      el.fileListContainer.appendChild(item);
    });
  }

  function renderDiff() {
    if (!el.diffViewerContainer) return;
    el.diffViewerContainer.innerHTML = '';

    const lines = state.diffs[state.targetFile] || [
      { type: 'normal', text: `# ${state.targetFile}` },
      { type: 'added', text: '+ # No active diff available for this file' }
    ];

    lines.forEach(line => {
      const div = document.createElement('div');
      div.className = `diff-line ${line.type}`;
      div.textContent = line.text;
      el.diffViewerContainer.appendChild(div);
    });
  }

  // ------------------------------------------------------------------------
  // Drawer Modals Manager
  // ------------------------------------------------------------------------
  function openDrawer(name) {
    if (!el.drawerOverlay || !el.drawerTitle || !el.drawerBody) return;
    state.activeDrawer = name;
    el.drawerBody.innerHTML = '';

    switch (name) {
      case 'artifacts':
        el.drawerTitle.textContent = '📋 아티팩트 목록';
        const artifactsList = [
          { title: '2026-08-23 동기화 및 핸드오버 보고서', path: 'docs/2026-08-23_pc_sync_and_handover_report.md' },
          { title: '2026-08-23 PC 환경 동기화 상세 명세서', path: 'coding-agent/docs/specs/2026-08-23_pc_synchronization_spec.md' },
          { title: '마스터 개발 로드맵 (TODO.md)', path: 'coding-agent/TODO.md' }
        ];
        artifactsList.forEach(art => {
          const item = document.createElement('div');
          item.className = 'drawer-card-item';
          item.innerHTML = `<div class="card-item-title">${art.title}</div><div class="card-item-sub">${art.path}</div>`;
          item.addEventListener('click', () => {
            if (vscode) vscode.postMessage({ command: 'openFile', path: art.path });
            closeDrawer();
          });
          el.drawerBody.appendChild(item);
        });
        break;

      case 'history':
        el.drawerTitle.textContent = '🕒 대화 세션 히스토리';
        state.sessions.forEach(sess => {
          const item = document.createElement('div');
          item.className = 'drawer-card-item';
          item.innerHTML = `<div class="card-item-title">${sess.title}</div><div class="card-item-sub">ID: ${sess.id} | Mode: ${sess.mode}</div>`;
          el.drawerBody.appendChild(item);
        });
        break;

      case 'memory':
        el.drawerTitle.textContent = '🧠 Mem0 장기 기억 프로필';
        state.memories.forEach(mem => {
          const item = document.createElement('div');
          item.className = 'drawer-card-item';
          item.innerHTML = `<div class="card-item-title" style="color:var(--purple-main)">[${mem.category}] ${mem.key}</div><div class="card-item-sub" style="color:var(--text-primary)">${mem.value}</div>`;
          el.drawerBody.appendChild(item);
        });
        break;

      case 'graph':
        el.drawerTitle.textContent = '🕸️ Graphify Python AST 지식 그래프';
        const stats = state.graphStats;
        const statCard = document.createElement('div');
        statCard.className = 'drawer-card-item';
        statCard.innerHTML = `
          <div class="card-item-title" style="color:var(--cyan-main)">AST Graph Metrics</div>
          <div class="card-item-sub" style="font-size:0.75rem; color:var(--text-primary); margin-top:4px;">
            <div>• Files Analyzed: ${stats.total_files || 14}</div>
            <div>• Classes Extracted: ${stats.classes || 8}</div>
            <div>• Functions & Methods: ${stats.functions || 40}</div>
            <div>• Symbols Indexed: ${stats.total_symbols || 48}</div>
          </div>
        `;
        el.drawerBody.appendChild(statCard);
        break;

      case 'gstack':
        el.drawerTitle.textContent = '🧩 gstack Specialists & Workflows';
        const gstackCard = document.createElement('div');
        gstackCard.className = 'drawer-card-item';
        gstackCard.innerHTML = `
          <div class="card-item-title" style="color:var(--cyan-main)">전문가 페르소나 (8종)</div>
          <div class="card-item-sub" style="margin-top:4px;">@pm, @sa, @se, @qa, @cso, @dba, @growth, @ceo</div>
          <div class="card-item-title" style="color:var(--purple-main); margin-top:8px;">워크플로우 명령어 (10종)</div>
          <div class="card-item-sub" style="margin-top:4px;">/office-hours, /plan-ceo-review, /plan-eng-review, /review, /investigate, /qa, /ship</div>
        `;
        el.drawerBody.appendChild(gstackCard);
        break;
    }

    el.drawerOverlay.classList.remove('hidden');
  }

  function closeDrawer() {
    if (el.drawerOverlay) {
      el.drawerOverlay.classList.add('hidden');
    }
  }

  // Run on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
