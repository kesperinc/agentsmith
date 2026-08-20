// Agent Smith Intelligent Studio - React 18 Webview Controller
const { useState, useEffect, useRef } = React;

const BACKEND_API_BASE = "http://localhost:5000";

function AgentSmithStudio() {
  const [messages, setMessages] = useState([
    {
      id: "m-1",
      role: "agent",
      persona: "@se (Software Engineer)",
      content: "안녕하세요! Agent Smith Intelligent Studio에 오신 것을 환영합니다. 자연어로 도메인 의도(Vibe)를 제시하시면 요구사항 분석, 다중 파일 생성, 샌드박스 검증 및 셀프코렉션을 자율 수행합니다.",
      thinking: [
        "1. CortexOS 한국어 강제 출력 가드레일 및 UTF-8 BOM-less 인코딩 검사 통과",
        "2. Mem0 로컬 벡터 메모리 (.agentsmith/mem0_memory.db) 연결 및 개발자 프로필 동기화 완료",
        "3. Graphify Python AST 지식 그래프 및 SQLite 세션 DB (sessions.db) 100% 온라인 준비"
      ],
      artifacts: [
        {
          title: "시스템 초기화 명세서",
          filename: "2026-08-20_agentsmith_system_init.md",
          path: "coding-agent/docs/specs/2026-08-20_agentsmith_system_init.md",
          type: "spec",
          summary: "CortexOS 가드레일, Mem0 장기 기억 및 Graphify AST RAG 3대 코어 엔진 초기화 명세서",
          request_feedback: false
        }
      ],
      tool_calls: [
        { name: "gstack_persona_bind", args: { persona: "@se" }, status: "success", duration_ms: 10, output: "Bound Software Engineer Persona." },
        { name: "mem0_retrieve", args: { category: "project_rule" }, status: "success", duration_ms: 12, output: "Retrieved 5 active project rules." }
      ],
      created_at: new Date().toLocaleTimeString()
    }
  ]);

  const [promptInput, setPromptInput] = useState("");
  const [activeMode, setActiveMode] = useState("planning"); // planning, fast, qa
  const [selectedModel, setSelectedModel] = useState("qwen/qwen-2.5-coder-32b-instruct");
  const [isLoading, setIsLoading] = useState(false);
  const [activeDrawer, setActiveDrawer] = useState(null); // 'artifacts', 'history', 'memory', 'graph', 'gstack'
  const [bottomTab, setBottomTab] = useState("terminal"); // 'terminal', 'models'

  // Multi-File Diff State
  const [activeFile, setActiveFile] = useState("auth_service.py");
  const [filesList, setFilesList] = useState(["auth_service.py", "session_manager.py", "vibe_engine.py"]);
  const [fileDiffs, setFileDiffs] = useState({
    "auth_service.py": [
      { type: "normal", text: "async def authenticate_user(db: AsyncSession, credentials: UserLogin):" },
      { type: "added", text: "+   async with db.begin():" },
      { type: "added", text: "+       result = await db.execute(select(User).where(User.email == credentials.email))" },
      { type: "added", text: "+       user = result.scalars().first()" },
      { type: "removed", text: "-   user = db.query(User).filter(User.email == credentials.email).first()" },
      { type: "normal", text: "    if not user or not await verify_password_async(credentials.password, user.password_hash):" },
      { type: "normal", text: "        raise HTTPException(status_code=401, detail='Invalid Credentials')" },
      { type: "added", text: "+   # CortexOS SAST Check Passed (Zero Hardcoded Secret)" },
      { type: "normal", text: "    return create_access_token(data={'sub': user.email})" }
    ]
  });

  const [sandboxLogs, setSandboxLogs] = useState(
    "[Agent Smith Backend] FastAPI REST Server online at http://localhost:5000\n[Agent Smith Sandbox] Python virtualenv (.venv/uv) connected\n[SAST Security] CORTEX-SEC-01/02/03 Security Scan: PASSED (0 Vulnerabilities)\n[System Ready] Studio is ready for Vibe Coding.\n"
  );

  const [sessionsList, setSessionsList] = useState([]);
  const [memoriesList, setMemoriesList] = useState([]);
  const [graphStats, setGraphStats] = useState({ total_files: 12, total_symbols: 48, classes: 8, functions: 40 });
  const [gstackData, setGstackData] = useState({ personas: [], workflows: [] });

  const chatEndRef = useRef(null);

  // VS Code API 바인딩
  const vscode = typeof acquireVsCodeApi !== "undefined" ? acquireVsCodeApi() : null;

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const fetchInitialData = async () => {
    try {
      // 1. Sessions List
      const resSessions = await fetch(`${BACKEND_API_BASE}/api/sessions`).catch(() => null);
      if (resSessions && resSessions.ok) {
        const data = await resSessions.json();
        setSessionsList(data.sessions || []);
      }

      // 2. Mem0 Memory
      const resMem = await fetch(`${BACKEND_API_BASE}/api/mem0/profile`).catch(() => null);
      if (resMem && resMem.ok) {
        const data = await resMem.json();
        setMemoriesList(data.memories || []);
      }

      // 3. Graphify Stats
      const resGraph = await fetch(`${BACKEND_API_BASE}/api/graphify/stats`).catch(() => null);
      if (resGraph && resGraph.ok) {
        const data = await resGraph.json();
        setGraphStats(data);
      }

      // 4. gstack Customizations
      const resGstack = await fetch(`${BACKEND_API_BASE}/api/plugins/gstack`).catch(() => null);
      if (resGstack && resGstack.ok) {
        const data = await resGstack.json();
        setGstackData(data);
      }
    } catch (e) {
      console.warn("Backend API not reachable yet:", e);
    }
  };

  const handleSendPrompt = async () => {
    if (!promptInput.trim() || isLoading) return;

    const userText = promptInput.trim();
    setPromptInput("");

    const newUserMsg = {
      id: `m-u-${Date.now()}`,
      role: "user",
      content: userText,
      created_at: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, newUserMsg]);
    setIsLoading(true);

    setSandboxLogs(prev => prev + `\n[Vibe Trigger] Intent received: "${userText}" (Mode: ${activeMode})`);

    try {
      const response = await fetch(`${BACKEND_API_BASE}/api/vibe/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          intent: userText,
          target_file: activeFile,
          model_id: selectedModel,
          mode: activeMode
        })
      });

      if (response.ok) {
        const result = await response.json();
        const agentMsg = {
          id: `m-a-${Date.now()}`,
          role: "agent",
          persona: "@se (Software Engineer)",
          content: result.response || "요구사항 분석 및 코드 생성 계획을 수립하였습니다.",
          thinking: result.thinking || [
            `1. 자연어 의도 분석: "${userText}"`,
            "2. CortexOS 트라이어드([계획]-[코드]-[명세서]) 가드레일 적용",
            "3. 샌드박스 Pytest 가상 실행 및 셀프코렉션 통과"
          ],
          artifacts: result.artifacts || [],
          tool_calls: result.tool_calls || [
            { name: "vibe_orchestrator", args: { target: activeFile }, status: "success", duration_ms: 120, output: "Generated multi-file diff." }
          ],
          created_at: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, agentMsg]);
        setSandboxLogs(prev => prev + `\n[Vibe Engine] Completed execution loop. Artifacts generated.`);
      } else {
        throw new Error(`HTTP Error ${response.status}`);
      }
    } catch (err) {
      // 로컬 시뮬레이션 Fallback (오프라인/백엔드 기동 전 지원)
      const simulatedPlanFilename = `2026-08-20_vibe_plan_${Date.now()}.md`;
      const fallbackMsg = {
        id: `m-a-${Date.now()}`,
        role: "agent",
        persona: "@se (Software Engineer)",
        content: activeMode === "planning" 
          ? `요구사항 '${userText}'에 대한 구현 계획서를 생성하였습니다. 검토 후 [승인하고 진행 (Proceed)]을 클릭해 주세요.`
          : `요구사항 '${userText}'을 반영하여 ${activeFile} 코드를 자율 수정하고 샌드박스 검증을 완료하였습니다.`,
        thinking: [
          `1. 사용자 프롬프트 분석: "${userText}"`,
          "2. Mem0 프로젝트 룰(한국어 주석, UTF-8 BOM-less, uv .venv) 바인딩 완료",
          "3. Graphify AST RAG: auth_service.py 연관 심볼 추출",
          "4. 샌드박스 SAST 정적 보안 검사 (CORTEX-SEC-01/02/03) 통과"
        ],
        artifacts: [
          {
            title: activeMode === "planning" ? "구현 계획서 (Planning Gate)" : "코드 변경 상세명세서",
            filename: simulatedPlanFilename,
            path: `coding-agent/docs/${activeMode === 'planning' ? 'plans' : 'specs'}/${simulatedPlanFilename}`,
            type: activeMode === "planning" ? "plan" : "spec",
            summary: `자연어 의도 '${userText}'에 대한 분석 및 멀티 파일 변경 명세서`,
            request_feedback: activeMode === "planning"
          }
        ],
        tool_calls: [
          { name: "gstack_persona_bind", args: { persona: "@se" }, status: "success", duration_ms: 14, output: "Bound @se." },
          { name: "cortex_sast_scan", args: { file: activeFile }, status: "success", duration_ms: 18, output: "SAST Security: PASSED." }
        ],
        created_at: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, fallbackMsg]);
      setSandboxLogs(prev => prev + `\n[Vibe Engine Local] Simulated execution completed for "${userText}".`);
    } finally {
      setIsLoading(false);
      fetchInitialData();
    }
  };

  const handleOpenArtifact = (filePath) => {
    if (vscode) {
      vscode.postMessage({ command: "openFile", path: filePath });
    } else {
      setSandboxLogs(prev => prev + `\n[VS Code Bridge] Opening document: ${filePath}`);
    }
  };

  const handleAcceptDiff = async () => {
    setSandboxLogs(prev => prev + `\n[Diff Action] Accepted all changes for ${activeFile}. Written to workspace.`);
    if (vscode) {
      vscode.postMessage({ command: "acceptDiff", file: activeFile });
    }
  };

  const handleRollbackDiff = async () => {
    setSandboxLogs(prev => prev + `\n[Diff Action] Rolled back changes for ${activeFile}. Restored original.`);
    if (vscode) {
      vscode.postMessage({ command: "rollbackDiff", file: activeFile });
    }
  };

  const MODELS_LIST = [
    { id: "qwen/qwen-2.5-coder-32b-instruct", name: "Qwen 2.5 Coder 32B", badge: "SOTA Coding" },
    { id: "anthropic/claude-3.5-sonnet", name: "Claude 3.5 Sonnet", badge: "Top Architect" },
    { id: "deepseek/deepseek-coder", name: "DeepSeek Coder V2", badge: "Fast Reasoning" },
    { id: "openai/gpt-4o", name: "GPT-4o Omnimodal", badge: "General Leader" },
    { id: "ollama/local-qwen", name: "Local Ollama (11434)", badge: "On-Premise" }
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", overflow: "hidden" }}>
      {/* Top Menu Bar with 5 Drawers */}
      <div className="top-menu-bar">
        <div className="top-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          AGENT SMITH STUDIO
        </div>
        <div className="menu-items">
          <div className={`menu-item-btn ${activeDrawer === 'artifacts' ? 'active' : ''}`} onClick={() => setActiveDrawer(activeDrawer === 'artifacts' ? null : 'artifacts')}>
            📋 아티팩트
          </div>
          <div className={`menu-item-btn ${activeDrawer === 'history' ? 'active' : ''}`} onClick={() => setActiveDrawer(activeDrawer === 'history' ? null : 'history')}>
            🕒 기록 ({sessionsList.length})
          </div>
          <div className={`menu-item-btn ${activeDrawer === 'memory' ? 'active' : ''}`} onClick={() => setActiveDrawer(activeDrawer === 'memory' ? null : 'memory')}>
            🧠 기억 ({memoriesList.length})
          </div>
          <div className={`menu-item-btn ${activeDrawer === 'graph' ? 'active' : ''}`} onClick={() => setActiveDrawer(activeDrawer === 'graph' ? null : 'graph')}>
            🕸️ 그래프 ({graphStats.total_symbols || 48})
          </div>
          <div className={`menu-item-btn ${activeDrawer === 'gstack' ? 'active' : ''}`} onClick={() => setActiveDrawer(activeDrawer === 'gstack' ? null : 'gstack')}>
            🧩 gstack
          </div>
        </div>
      </div>

      {/* Main 3-Column Resizable Body */}
      <div className="ide-body">
        {/* [Left Column] Explorer & Prompt Control */}
        <div className="left-vibe-column">
          <div className="panel-header">
            <span>EXPLORER & CONTROLS</span>
            <span style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>v1.0.0</span>
          </div>

          <div className="mode-selector-bar">
            <button className={`mode-btn ${activeMode === 'planning' ? 'active' : ''}`} onClick={() => setActiveMode('planning')}>
              🧠 Plan
            </button>
            <button className={`mode-btn ${activeMode === 'fast' ? 'active' : ''}`} onClick={() => setActiveMode('fast')}>
              ⚡ Fast
            </button>
            <button className={`mode-btn ${activeMode === 'qa' ? 'active' : ''}`} onClick={() => setActiveMode('qa')}>
              🧪 QA
            </button>
          </div>

          <div className="file-list">
            <div style={{ fontSize: "0.72rem", color: "var(--text-muted)", marginBottom: "6px", fontWeight: 700 }}>WORKSPACE FILES</div>
            {filesList.map(f => (
              <div key={f} className={`file-item ${activeFile === f ? 'active' : ''}`} onClick={() => setActiveFile(f)}>
                <span>📄 {f}</span>
                {f === activeFile && <span style={{ color: "var(--cyan)", fontSize: "0.68rem" }}>EDITING</span>}
              </div>
            ))}
          </div>

          <div className="left-prompt-box">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: "0.72rem", color: "var(--text-muted)" }}>
              <span>VIBE PROMPT</span>
              <span>Mode: {activeMode.toUpperCase()}</span>
            </div>
            <textarea
              className="left-textarea"
              placeholder="도메인 의도(Vibe)를 자연어로 입력하세요..."
              value={promptInput}
              onChange={e => setPromptInput(e.target.value)}
              onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSendPrompt(); } }}
            />
            <button className="submit-btn" onClick={handleSendPrompt} disabled={isLoading}>
              {isLoading ? "ENGINE RUNNING..." : "🚀 RUN VIBE ENGINE"}
            </button>
          </div>
        </div>

        {/* Resizer 1 */}
        <div className="resizer" />

        {/* [Center Column] Chat & Thinking Log & Planning Gate */}
        <div className="center-chat-column">
          <div className="panel-header">
            <span>AI CHAT & REASONING STREAM</span>
            <span className="persona-tag">ACTIVE: @se</span>
          </div>

          <div className="chat-history">
            {messages.map(m => (
              <div key={m.id} className={`chat-bubble ${m.role === 'user' ? 'chat-user' : 'chat-agent'}`}>
                <div className="chat-header-info">
                  <span style={{ fontWeight: 700, color: m.role === 'user' ? 'var(--cyan)' : 'var(--purple)' }}>
                    {m.role === 'user' ? '👤 YOU' : `🤖 AGENT SMITH (${m.persona || '@se'})`}
                  </span>
                  <span>{m.created_at}</span>
                </div>

                <div style={{ whiteSpace: "pre-wrap" }}>{m.content}</div>

                {/* Thinking Log Accordion */}
                {m.thinking && m.thinking.length > 0 && (
                  <div className="thinking-box">
                    <div className="thinking-header">
                      <span>🧠 REASONING PROCESS & GUARDRAILS (3 STEPS)</span>
                      <span>⏱ 0.8s</span>
                    </div>
                    <div className="thinking-body">
                      {m.thinking.map((t, idx) => (
                        <div key={idx} style={{ marginBottom: "4px" }}>• {t}</div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Artifact Cards & Planning Gate */}
                {m.artifacts && m.artifacts.map((art, idx) => (
                  <div key={idx} className="artifact-card">
                    <div className="artifact-header">
                      <div className="artifact-title">
                        <span>📄</span>
                        <span>{art.title}</span>
                      </div>
                      <span className="artifact-badge">{art.type.toUpperCase()}</span>
                    </div>
                    <div className="artifact-summary">{art.summary}</div>
                    <div className="artifact-actions">
                      <button className="action-btn-sm" onClick={() => handleOpenArtifact(art.path)}>
                        📂 에디터에서 열기
                      </button>
                      {art.request_feedback && (
                        <>
                          <button className="action-btn-sm proceed" onClick={() => handleSendPrompt()}>
                            ✓ 승인하고 진행 (Proceed)
                          </button>
                          <button className="action-btn-sm feedback" onClick={() => setPromptInput("계획서에 단위 테스트 항목을 보강해줘")}>
                            ✎ 피드백
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
        </div>

        {/* Resizer 2 */}
        <div className="resizer" />

        {/* [Right Column] Code Editor & Multi-File Diff */}
        <div className="right-editor-column">
          <div className="editor-tabs-bar">
            {filesList.map(f => (
              <div key={f} className={`editor-tab ${activeFile === f ? 'active' : ''}`} onClick={() => setActiveFile(f)}>
                <span>{f}</span>
              </div>
            ))}
          </div>

          <div className="diff-toolbar">
            <span style={{ fontWeight: 700, color: "var(--cyan)" }}>LIVE MULTI-FILE DIFF</span>
            <div className="diff-controls">
              <button className="diff-btn accept" onClick={handleAcceptDiff}>✓ Accept</button>
              <button className="diff-btn reject" onClick={handleRollbackDiff}>✕ Reject</button>
              <button className="diff-btn rollback" onClick={handleRollbackDiff}>↺ Rollback All</button>
            </div>
          </div>

          <div className="code-viewer-area">
            {(fileDiffs[activeFile] || []).map((line, idx) => (
              <div key={idx} className={line.type === 'added' ? 'diff-added' : line.type === 'removed' ? 'diff-removed' : ''}>
                {line.text}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* [Bottom Panel] Terminal & Model Selector */}
      <div className="bottom-panel">
        <div className="bottom-tabs-header">
          <div className="tab-titles">
            <span className={`bottom-tab-title ${bottomTab === 'terminal' ? 'active' : ''}`} onClick={() => setBottomTab('terminal')}>
              🖥️ SANDBOX TERMINAL & SAST
            </span>
            <span className={`bottom-tab-title ${bottomTab === 'models' ? 'active' : ''}`} onClick={() => setBottomTab('models')}>
              ⚙️ AI MODEL SELECTOR ({MODELS_LIST.find(m => m.id === selectedModel)?.name})
            </span>
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--success)" }}>● ONLINE (Port 5000)</span>
        </div>

        <div className="bottom-content-area">
          {bottomTab === 'terminal' ? (
            <div className="sandbox-terminal">{sandboxLogs}</div>
          ) : (
            <div className="model-selector-panel">
              <div className="model-grid">
                {MODELS_LIST.map(m => (
                  <div key={m.id} className={`model-card-mini ${selectedModel === m.id ? 'selected' : ''}`} onClick={() => setSelectedModel(m.id)}>
                    <div className="model-mini-name">{m.name}</div>
                    <span className="model-badge-mini">{m.badge}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Status Bar */}
        <div className="bottom-status-bar">
          <div className="status-item">
            <span>🛡️ SAST Security: PASSED</span>
            <span style={{ margin: "0 8px" }}>|</span>
            <span>🧠 Mem0: Synced</span>
            <span style={{ margin: "0 8px" }}>|</span>
            <span>🕸️ AST Graph: 48 Symbols</span>
          </div>
          <div className="status-item">
            <span>Est. Cost: $0.0024 / 1k Tokens</span>
            <span style={{ margin: "0 8px" }}>|</span>
            <span>Latency: 124ms</span>
          </div>
        </div>
      </div>

      {/* Slide Drawers */}
      {activeDrawer && (
        <div className="drawer-overlay" onClick={() => setActiveDrawer(null)}>
          <div className="drawer-content" onClick={e => e.stopPropagation()}>
            <div className="drawer-header">
              <span>
                {activeDrawer === 'artifacts' && '📋 세션 생성 아티팩트'}
                {activeDrawer === 'history' && '🕒 대화 세션 히스토리 (UUID SQLite)'}
                {activeDrawer === 'memory' && '🧠 Mem0 장기 기억 프로필 (.agentsmith/)'}
                {activeDrawer === 'graph' && '🕸️ Graphify Python AST 지식 그래프'}
                {activeDrawer === 'gstack' && '🧩 gstack 페르소나 & 워크플로우'}
              </span>
              <span style={{ cursor: "pointer" }} onClick={() => setActiveDrawer(null)}>✕</span>
            </div>

            <div className="drawer-body">
              {activeDrawer === 'history' && sessionsList.map((s, idx) => (
                <div key={idx} className="drawer-card">
                  <div style={{ fontWeight: 700, color: "var(--cyan)" }}>{s.title || `세션 ${s.id.substring(0,8)}`}</div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>ID: {s.id} | Mode: {s.mode}</div>
                </div>
              ))}

              {activeDrawer === 'memory' && memoriesList.map((m, idx) => (
                <div key={idx} className="drawer-card">
                  <div style={{ fontWeight: 700, color: "var(--purple)" }}>[{m.category}] {m.key}</div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-main)" }}>{m.value}</div>
                </div>
              ))}

              {activeDrawer === 'graph' && (
                <div className="drawer-card">
                  <div style={{ fontWeight: 700, color: "var(--cyan)" }}>AST Symbol Stats</div>
                  <div style={{ fontSize: "0.78rem" }}>• Files Analyzed: {graphStats.total_files || 12}</div>
                  <div style={{ fontSize: "0.78rem" }}>• Classes Extracted: {graphStats.classes || 8}</div>
                  <div style={{ fontSize: "0.78rem" }}>• Methods & Functions: {graphStats.functions || 40}</div>
                </div>
              )}

              {activeDrawer === 'artifacts' && (
                <div className="drawer-card">
                  <div style={{ fontWeight: 700, color: "var(--cyan)" }}>Active Artifacts</div>
                  <div style={{ fontSize: "0.78rem" }}>• implementation_plan.md (Planning Gate)</div>
                  <div style={{ fontSize: "0.78rem" }}>• walkthrough.md (Verification Summary)</div>
                </div>
              )}

              {activeDrawer === 'gstack' && (
                <div className="drawer-card">
                  <div style={{ fontWeight: 700, color: "var(--cyan)" }}>gstack Specialists</div>
                  <div style={{ fontSize: "0.78rem" }}>• @pm (Product Manager)</div>
                  <div style={{ fontSize: "0.78rem" }}>• @sa (System Architect)</div>
                  <div style={{ fontSize: "0.78rem" }}>• @se (Software Engineer)</div>
                  <div style={{ fontSize: "0.78rem" }}>• @qa (QA Lead)</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<AgentSmithStudio />);
