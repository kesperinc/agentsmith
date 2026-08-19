(function () {
    // 🌐 VS Code Webview 및 브라우저 단독 실행(Direct Browser) 호환 브리지
    const isVsCode = typeof acquireVsCodeApi === 'function';
    const vscode = isVsCode ? acquireVsCodeApi() : {
        postMessage: function(msg) {
            console.log('[Browser Fallback Bridge]', msg);
            if (msg.command === 'sendVibe') {
                fetch('/api/vibe/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ intent: msg.intent, model_id: msg.modelId, mode: msg.mode, target_file: msg.targetFile })
                })
                .then(res => res.json())
                .then(data => {
                    window.dispatchEvent(new MessageEvent('message', { data: { command: 'sendVibeResponse', success: true, data: data } }));
                })
                .catch(err => {
                    window.dispatchEvent(new MessageEvent('message', { data: { command: 'sendVibeResponse', success: false, error: err.message } }));
                });
            } else if (msg.command === 'listSessions') {
                fetch('/api/sessions')
                .then(res => res.json())
                .then(data => {
                    window.dispatchEvent(new MessageEvent('message', { data: { command: 'sessionsListResponse', success: true, sessions: data.sessions } }));
                });
            } else if (msg.command === 'getMem0') {
                fetch('/api/mem0/profile')
                .then(res => res.json())
                .then(data => {
                    window.dispatchEvent(new MessageEvent('message', { data: { command: 'mem0ProfileResponse', success: true, memories: data.memories } }));
                });
            } else if (msg.command === 'getGraphify') {
                fetch('/api/graphify/stats')
                .then(res => res.json())
                .then(data => {
                    window.dispatchEvent(new MessageEvent('message', { data: { command: 'graphifyStatsResponse', success: true, data: data } }));
                });
            } else if (msg.command === 'getGstack') {
                fetch('/api/plugins/gstack')
                .then(res => res.json())
                .then(data => {
                    window.dispatchEvent(new MessageEvent('message', { data: { command: 'gstackPluginsResponse', success: true, data: data } }));
                });
            } else if (msg.command === 'scanArtifacts') {
                window.dispatchEvent(new MessageEvent('message', { data: { command: 'artifactsScanned', artifacts: [
                    { title: "2026-08-19_vibe_plan.md", filename: "2026-08-19_vibe_plan.md", path: "coding-agent/docs/plans/2026-08-19_vibe_plan.md", type: "plan", summary: "작업 계획서 아티팩트", request_feedback: true },
                    { title: "2026-08-19_vibe_spec.md", filename: "2026-08-19_vibe_spec.md", path: "coding-agent/docs/specs/2026-08-19_vibe_spec.md", type: "spec", summary: "상세 명세서 아티팩트", request_feedback: false }
                ] } }));
            }
        }
    };
    
    // UI Elements
    const authOverlay = document.getElementById('auth-overlay');
    const emailSection = document.getElementById('email-section');
    const otpSection = document.getElementById('otp-section');
    const authEmail = document.getElementById('auth-email');
    const authOtp = document.getElementById('auth-otp');
    const btnSendOtp = document.getElementById('btn-send-otp');
    const btnVerifyOtp = document.getElementById('btn-verify-otp');
    const btnBackEmail = document.getElementById('btn-back-email');
    const btnCloseAuth = document.getElementById('btn-close-auth');
    const btnSkipAuth = document.getElementById('btn-skip-auth');
    const btnToggleAuth = document.getElementById('btn-toggle-auth');
    const authBadge = document.getElementById('auth-badge');
    const authMessage = document.getElementById('auth-message');
    
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const autocompletePopup = document.getElementById('autocomplete-popup');
    const btnMic = document.getElementById('btn-mic');
    const btnSend = document.getElementById('btn-send');
    const btnNewChat = document.getElementById('btn-new-chat');
    const modelSelect = document.getElementById('model-select');
    const modeSelect = document.getElementById('mode-select');

    // 📋 아티팩트 드로어 Elements
    const artifactsDrawer = document.getElementById('artifacts-drawer');
    const btnToggleArtifacts = document.getElementById('btn-toggle-artifacts');
    const btnCloseDrawer = document.getElementById('btn-close-drawer');
    const btnRefreshArtifacts = document.getElementById('btn-refresh-artifacts');
    const artifactsCount = document.getElementById('artifacts-count');
    const drawerArtifactsList = document.getElementById('drawer-artifacts-list');

    // 🕒 세션 히스토리 드로어 Elements
    const sessionsDrawer = document.getElementById('sessions-drawer');
    const btnToggleSessions = document.getElementById('btn-toggle-sessions');
    const btnCloseSessions = document.getElementById('btn-close-sessions');
    const btnRefreshSessions = document.getElementById('btn-refresh-sessions');
    const drawerSessionsList = document.getElementById('drawer-sessions-list');

    // 🧠 Mem0 드로어 Elements
    const mem0Drawer = document.getElementById('mem0-drawer');
    const btnToggleMem0 = document.getElementById('btn-toggle-mem0');
    const btnCloseMem0 = document.getElementById('btn-close-mem0');
    const btnRefreshMem0 = document.getElementById('btn-refresh-mem0');
    const drawerMem0List = document.getElementById('drawer-mem0-list');

    // 🕸️ Graphify 드로어 Elements
    const graphifyDrawer = document.getElementById('graphify-drawer');
    const btnToggleGraphify = document.getElementById('btn-toggle-graphify');
    const btnCloseGraphify = document.getElementById('btn-close-graphify');
    const btnRefreshGraphify = document.getElementById('btn-refresh-graphify');
    const drawerGraphifyList = document.getElementById('drawer-graphify-list');

    // 🧩 gstack 플러그인 드로어 Elements
    const pluginsDrawer = document.getElementById('plugins-drawer');
    const btnTogglePlugins = document.getElementById('btn-toggle-plugins');
    const btnClosePlugins = document.getElementById('btn-close-plugins');
    const btnRefreshPlugins = document.getElementById('btn-refresh-plugins');
    const drawerPluginsList = document.getElementById('drawer-plugins-list');

    let currentEmail = '';
    let isRecording = false;
    let sessionArtifacts = [];
    let activeSessionDiffs = [];
    let gstackData = { personas: [], workflows: [] };

    // ==========================================
    // 0. 초기화 및 워크스페이스 스캔
    // ==========================================
    vscode.postMessage({ command: 'scanArtifacts' });
    vscode.postMessage({ command: 'listSessions' });
    vscode.postMessage({ command: 'getMem0' });
    vscode.postMessage({ command: 'getGraphify' });
    vscode.postMessage({ command: 'getGstack' });

    // ==========================================
    // 1. 드로어 제어 (아티팩트 / 세션 / Mem0 / Graphify / gstack)
    // ==========================================
    function closeAllDrawers() {
        if (artifactsDrawer) artifactsDrawer.classList.remove('active');
        if (sessionsDrawer) sessionsDrawer.classList.remove('active');
        if (mem0Drawer) mem0Drawer.classList.remove('active');
        if (graphifyDrawer) graphifyDrawer.classList.remove('active');
        if (pluginsDrawer) pluginsDrawer.classList.remove('active');
    }

    if (btnToggleArtifacts) {
        btnToggleArtifacts.addEventListener('click', () => {
            const wasActive = artifactsDrawer.classList.contains('active');
            closeAllDrawers();
            if (!wasActive) artifactsDrawer.classList.add('active');
        });
    }

    if (btnCloseDrawer) {
        btnCloseDrawer.addEventListener('click', () => {
            artifactsDrawer.classList.remove('active');
        });
    }

    if (btnRefreshArtifacts) {
        btnRefreshArtifacts.addEventListener('click', () => {
            vscode.postMessage({ command: 'scanArtifacts' });
        });
    }

    if (btnToggleSessions) {
        btnToggleSessions.addEventListener('click', () => {
            const wasActive = sessionsDrawer.classList.contains('active');
            closeAllDrawers();
            if (!wasActive) {
                sessionsDrawer.classList.add('active');
                vscode.postMessage({ command: 'listSessions' });
            }
        });
    }

    if (btnCloseSessions) {
        btnCloseSessions.addEventListener('click', () => {
            sessionsDrawer.classList.remove('active');
        });
    }

    if (btnRefreshSessions) {
        btnRefreshSessions.addEventListener('click', () => {
            vscode.postMessage({ command: 'listSessions' });
        });
    }

    if (btnToggleMem0) {
        btnToggleMem0.addEventListener('click', () => {
            const wasActive = mem0Drawer.classList.contains('active');
            closeAllDrawers();
            if (!wasActive) {
                mem0Drawer.classList.add('active');
                vscode.postMessage({ command: 'getMem0' });
            }
        });
    }

    if (btnCloseMem0) {
        btnCloseMem0.addEventListener('click', () => {
            mem0Drawer.classList.remove('active');
        });
    }

    if (btnRefreshMem0) {
        btnRefreshMem0.addEventListener('click', () => {
            vscode.postMessage({ command: 'getMem0' });
        });
    }

    if (btnToggleGraphify) {
        btnToggleGraphify.addEventListener('click', () => {
            const wasActive = graphifyDrawer.classList.contains('active');
            closeAllDrawers();
            if (!wasActive) {
                graphifyDrawer.classList.add('active');
                vscode.postMessage({ command: 'getGraphify' });
            }
        });
    }

    if (btnCloseGraphify) {
        btnCloseGraphify.addEventListener('click', () => {
            graphifyDrawer.classList.remove('active');
        });
    }

    if (btnRefreshGraphify) {
        btnRefreshGraphify.addEventListener('click', () => {
            vscode.postMessage({ command: 'getGraphify' });
        });
    }

    if (btnTogglePlugins) {
        btnTogglePlugins.addEventListener('click', () => {
            const wasActive = pluginsDrawer.classList.contains('active');
            closeAllDrawers();
            if (!wasActive) {
                pluginsDrawer.classList.add('active');
                vscode.postMessage({ command: 'getGstack' });
            }
        });
    }

    if (btnClosePlugins) {
        btnClosePlugins.addEventListener('click', () => {
            pluginsDrawer.classList.remove('active');
        });
    }

    if (btnRefreshPlugins) {
        btnRefreshPlugins.addEventListener('click', () => {
            vscode.postMessage({ command: 'getGstack' });
        });
    }

    // ==========================================
    // 2. 사내 인증 모달 제어
    // ==========================================
    if (btnToggleAuth) {
        btnToggleAuth.addEventListener('click', () => {
            authOverlay.classList.toggle('active');
        });
    }

    if (btnCloseAuth) {
        btnCloseAuth.addEventListener('click', () => {
            authOverlay.classList.remove('active');
        });
    }

    if (btnSkipAuth) {
        btnSkipAuth.addEventListener('click', () => {
            authOverlay.classList.remove('active');
        });
    }

    // ==========================================
    // 3. 새 대화 시작 (New Chat)
    // ==========================================
    if (btnNewChat) {
        btnNewChat.addEventListener('click', () => {
            chatMessages.innerHTML = `
                <div class="message system-msg">
                    <strong>[시스템]</strong> 새 세션이 시작되었습니다. (Planning Mode, Live Multi-File Diff, 🧩 gstack, 🧠 Mem0 및 🕸️ Graphify 준비 완료)
                </div>
            `;
            sessionArtifacts = [];
            activeSessionDiffs = [];
            updateDrawerList();
            vscode.postMessage({ command: 'newChat' });
        });
    }

    // ==========================================
    // 4. 이메일 OTP 인증 처리
    // ==========================================
    if (btnSendOtp) {
        btnSendOtp.addEventListener('click', () => {
            const email = authEmail.value.trim();
            if (!email || !email.includes('@')) {
                showAuthError('올바른 사내 이메일 주소를 입력하세요.');
                return;
            }
            currentEmail = email;
            authMessage.textContent = 'OTP 코드 전송 중...';
            vscode.postMessage({
                command: 'sendOtp',
                email: email
            });
        });
    }

    if (btnVerifyOtp) {
        btnVerifyOtp.addEventListener('click', () => {
            const otp = authOtp.value.trim();
            if (otp.length !== 6 || isNaN(otp)) {
                showAuthError('숫자 6자리 보안코드를 입력해 주세요.');
                return;
            }
            authMessage.textContent = '인증번호 검증 중...';
            vscode.postMessage({
                command: 'verifyOtp',
                email: currentEmail,
                otpCode: otp
            });
        });
    }

    if (btnBackEmail) {
        btnBackEmail.addEventListener('click', () => {
            otpSection.classList.remove('active');
            emailSection.classList.add('active');
            authOtp.value = '';
            authMessage.textContent = '';
        });
    }

    // ==========================================
    // ⚡ 5. @ 및 / 인터랙티브 자동완성 (Autocomplete) 로직
    // ==========================================
    let activeSuggestions = [];
    let selectedIndex = 0;

    chatInput.addEventListener('input', () => {
        const val = chatInput.value;
        const cursor = chatInput.selectionStart;
        const textBeforeCursor = val.slice(0, cursor);
        const lastWordMatch = textBeforeCursor.match(/([@/][a-zA-Z0-9_\-]*)$/);

        if (lastWordMatch) {
            const query = lastWordMatch[1];
            if (query.startsWith('@')) {
                const filter = query.toLowerCase();
                activeSuggestions = gstackData.personas.filter(p => p.id.toLowerCase().includes(filter));
                renderAutocomplete(activeSuggestions, 'persona', query);
            } else if (query.startsWith('/')) {
                const filter = query.toLowerCase();
                activeSuggestions = gstackData.workflows.filter(w => w.command.toLowerCase().includes(filter));
                renderAutocomplete(activeSuggestions, 'workflow', query);
            }
        } else {
            hideAutocomplete();
        }
    });

    chatInput.addEventListener('keydown', (e) => {
        if (autocompletePopup.classList.contains('active') && activeSuggestions.length > 0) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedIndex = (selectedIndex + 1) % activeSuggestions.length;
                updateSelectedAutocomplete();
                return;
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedIndex = (selectedIndex - 1 + activeSuggestions.length) % activeSuggestions.length;
                updateSelectedAutocomplete();
                return;
            } else if (e.key === 'Enter' || e.key === 'Tab') {
                e.preventDefault();
                selectSuggestion(activeSuggestions[selectedIndex]);
                return;
            } else if (e.key === 'Escape') {
                hideAutocomplete();
                return;
            }
        }

        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendUserMessage();
        }
    });

    function renderAutocomplete(items, type, query) {
        if (!items || items.length === 0) {
            hideAutocomplete();
            return;
        }
        selectedIndex = 0;
        autocompletePopup.innerHTML = items.map((item, idx) => {
            const isPersona = type === 'persona';
            const label = isPersona ? item.id : item.command;
            const subLabel = isPersona ? item.name : item.name;
            const desc = item.desc || '';
            return `
                <div class="autocomplete-item ${idx === 0 ? 'selected' : ''}" data-idx="${idx}">
                    <div class="autocomplete-left">
                        <span>${item.icon || (isPersona ? '🧭' : '⚡')}</span>
                        <span class="autocomplete-id ${isPersona ? '' : 'workflow'}">${label}</span>
                        <span style="font-size:0.75rem; color:#ffffff;">${subLabel}</span>
                    </div>
                    <span class="autocomplete-desc">${desc}</span>
                </div>
            `;
        }).join('');

        autocompletePopup.classList.add('active');

        autocompletePopup.querySelectorAll('.autocomplete-item').forEach(el => {
            el.addEventListener('click', () => {
                const idx = parseInt(el.getAttribute('data-idx'));
                selectSuggestion(items[idx]);
            });
        });
    }

    function updateSelectedAutocomplete() {
        const items = autocompletePopup.querySelectorAll('.autocomplete-item');
        items.forEach((el, idx) => {
            el.classList.toggle('selected', idx === selectedIndex);
        });
    }

    function selectSuggestion(item) {
        if (!item) return;
        const val = chatInput.value;
        const cursor = chatInput.selectionStart;
        const textBefore = val.slice(0, cursor);
        const textAfter = val.slice(cursor);
        
        const isPersona = !!item.id;
        const replacement = isPersona ? item.id : item.command;
        const updatedBefore = textBefore.replace(/([@/][a-zA-Z0-9_\-]*)$/, replacement + ' ');

        chatInput.value = updatedBefore + textAfter;
        chatInput.selectionStart = chatInput.selectionEnd = updatedBefore.length;
        chatInput.focus();
        hideAutocomplete();
    }

    function hideAutocomplete() {
        autocompletePopup.classList.remove('active');
        activeSuggestions = [];
    }

    // ==========================================
    // 6. 메시지 발송
    // ==========================================
    btnSend.addEventListener('click', sendUserMessage);

    function sendUserMessage() {
        const intent = chatInput.value.trim();
        if (!intent) return;

        appendMessage('user', intent);
        chatInput.value = '';
        hideAutocomplete();
        
        const modelId = modelSelect.value;
        const mode = modeSelect.value;
        appendMessage('system', `에이전트가 <strong>${mode === 'planning' ? 'Planning Mode' : mode === 'review' ? 'QA & Review Mode' : 'Direct Mode'}</strong>로 작업을 분석하고 있습니다...`);

        vscode.postMessage({
            command: 'sendVibe',
            intent: intent,
            modelId: modelId,
            mode: mode,
            targetFile: "auth_service.py"
        });
    }

    // ==========================================
    // 7. 음성 인식 (STT)
    // ==========================================
    let mediaRecorder = null;
    let audioChunks = [];

    btnMic.addEventListener('click', async () => {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioChunks = [];
                mediaRecorder = new MediaRecorder(stream);
                
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = () => {
                        const base64Data = reader.result.split(',')[1];
                        appendMessage('system', '음성 데이터를 텍스트로 변환(STT) 중입니다...');
                        vscode.postMessage({
                            command: 'audioData',
                            data: base64Data
                        });
                    };
                });

                mediaRecorder.start();
                isRecording = true;
                btnMic.classList.add('recording');
                btnMic.title = '음성 녹음 중... 클릭 시 완료';
            } catch (err) {
                appendMessage('system', `마이크 접근 실패: ${err.message}`);
            }
        } else {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
                isRecording = false;
                btnMic.classList.remove('recording');
                btnMic.title = '음성 인식 지시 (STT)';
            }
        }
    });

    // ==========================================
    // 8. VS Code & Browser 메시지 수신 핸들러
    // ==========================================
    window.addEventListener('message', event => {
        const message = event.data;
        switch (message.command) {
            case 'sendOtpResponse':
                if (message.success) {
                    emailSection.classList.remove('active');
                    otpSection.classList.add('active');
                    authMessage.textContent = '인증번호(6자리)가 발송되었습니다.';
                } else {
                    showAuthError(message.error || 'OTP 전송에 실패했습니다.');
                }
                break;
            case 'verifyOtpResponse':
                if (message.success) {
                    authOverlay.classList.remove('active');
                    if (authBadge) {
                        authBadge.textContent = '사내 인증됨';
                        authBadge.className = 'auth-badge enterprise';
                        authBadge.title = `사내 인증 계정: ${currentEmail}`;
                    }
                    appendMessage('system', `[인증 완료] 사내 메일 계정(${currentEmail})으로 성공적으로 연동되었습니다.`);
                } else {
                    showAuthError(message.error || '잘못된 보안코드이거나 만료되었습니다.');
                }
                break;
            case 'sendVibeResponse':
                removeSystemLoadingMessage();
                if (message.success) {
                    const res = message.data;
                    appendAgentResponse(res);
                } else {
                    appendMessage('agent', `[에러 발생] Vibe 코드 생성 실패: ${message.error}`);
                }
                break;
            case 'artifactsScanned':
                if (message.artifacts) {
                    sessionArtifacts = message.artifacts;
                    updateDrawerList();
                }
                break;
            case 'sessionsListResponse':
                if (message.sessions) {
                    renderSessionsList(message.sessions);
                }
                break;
            case 'sessionLoadedResponse':
                if (message.success && message.data) {
                    loadSessionData(message.data);
                }
                break;
            case 'mem0ProfileResponse':
                if (message.memories) {
                    renderMem0List(message.memories);
                }
                break;
            case 'graphifyStatsResponse':
                if (message.data) {
                    renderGraphifyStats(message.data);
                }
                break;
            case 'gstackPluginsResponse':
                if (message.data) {
                    gstackData = message.data;
                    renderGstackPlugins(message.data);
                }
                break;
            case 'diffAppliedResponse':
                updateDiffStatusInUi(message.filePath, 'accepted');
                break;
            case 'diffRolledBackResponse':
                updateDiffStatusInUi(message.filePath, 'rolled_back');
                break;
            case 'sttResponse':
                if (message.success && message.text) {
                    chatInput.value = message.text;
                    appendMessage('system', `[STT 변환 완료] "${message.text}"`);
                } else {
                    appendMessage('system', `[STT 변환 실패] ${message.error || '음성을 텍스트로 치환하지 못했습니다.'}`);
                }
                break;
        }
    });

    function showAuthError(msg) {
        authMessage.textContent = msg;
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', `${sender}-msg`);
        msgDiv.innerHTML = text.replace(/\n/g, '<br>');
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeSystemLoadingMessage() {
        const msgs = chatMessages.querySelectorAll('.system-msg');
        for (let i = msgs.length - 1; i >= 0; i--) {
            if (msgs[i].textContent.includes('분석하고 있습니다')) {
                msgs[i].remove();
                break;
            }
        }
    }

    // ==========================================
    // 9. 에이전트 응답 렌더러 (Persona, SAST, Thinking, Tools, Diff, RAG, Mem0)
    // ==========================================
    function appendAgentResponse(res) {
        const responseBox = document.createElement('div');
        responseBox.classList.add('message', 'agent-msg');

        let html = '';

        // 🧭 0. 활성 페르소나 및 SAST 보안 뱃지 표시
        if (res.persona || res.command || res.sast_result) {
            html += `<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">`;
            if (res.persona || res.command) {
                html += `<span class="persona-tag-active">🧭 <strong>${escapeHtml(res.persona || '@se')}</strong> ${res.command ? `(${escapeHtml(res.command)})` : ''}</span>`;
            } else {
                html += `<span></span>`;
            }
            if (res.sast_result) {
                const statusClass = res.sast_result.status === 'passed' ? 'passed' : 'warning';
                html += `<span class="sast-badge ${statusClass}">🛡️ SAST Security: ${res.sast_result.status.toUpperCase()}</span>`;
            }
            html += `</div>`;
        }
        
        // 🧠 1. 사고 과정 (Thinking Process) 접이식 아코디언 + 타이머
        if (res.thinking && res.thinking.length > 0) {
            const timerLabel = res.elapsed_seconds ? `⏱ ${res.elapsed_seconds}s` : '⏱ 3.2s';
            html += `
                <div class="accordion-block">
                    <div class="accordion-header" onclick="this.nextElementSibling.classList.toggle('collapsed')">
                        <span>🧠 사고 과정 (Thinking Process)</span>
                        <div style="display:flex; align-items:center; gap:6px;">
                            <span class="thinking-timer">${timerLabel}</span>
                            <span style="font-size:0.7rem; color:var(--cyan);">▼</span>
                        </div>
                    </div>
                    <div class="accordion-body">
                        ${res.thinking.map(step => `• ${escapeHtml(step)}`).join('<br>')}
                    </div>
                </div>
            `;
        }

        // 🛠️ 2. 실행된 도구 (Tool Calls) 아코디언 시각화
        if (res.tool_calls && res.tool_calls.length > 0) {
            html += `
                <div class="accordion-block">
                    <div class="accordion-header" onclick="this.nextElementSibling.classList.toggle('collapsed')">
                        <span>🛠️ 도구 호출 (Tool Calls - ${res.tool_calls.length}건)</span>
                        <span style="font-size:0.7rem; color:var(--cyan);">▼</span>
                    </div>
                    <div class="accordion-body">
                        ${res.tool_calls.map(tc => `
                            <div class="tool-call-item">
                                <div class="tool-call-header">
                                    <span>⚡ ${escapeHtml(tc.name)}</span>
                                    <span class="tool-badge ${tc.status || 'success'}">${tc.status ? tc.status.toUpperCase() : 'SUCCESS'} (${tc.duration_ms || 45}ms)</span>
                                </div>
                                <div class="tool-args">${escapeHtml(JSON.stringify(tc.args || {}))}</div>
                                <div style="font-size:0.72rem; color:var(--text-muted); margin-top:4px;">${escapeHtml(tc.output || '')}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        // 🔄 3. 셀프코렉션 (Self-Correction) 시각화
        if (res.self_correction) {
            html += `
                <div class="self-correction-box">
                    <div class="self-correction-title">
                        <span>🔄</span>
                        <span>자율 셀프코렉션 (Self-Correction Loop)</span>
                    </div>
                    <div class="correction-step">⚠️ <strong>감지된 오류:</strong> ${escapeHtml(res.self_correction.detected_error)}</div>
                    <div class="correction-step fixed">✓ <strong>자동 수정 조치:</strong> ${escapeHtml(res.self_correction.fixed_solution)}</div>
                </div>
            `;
        }

        // ⏳ 4. Planning Gate 승인 대기 배너 (Planning Mode일 때)
        if (res.is_waiting_approval) {
            html += `
                <div class="approval-gate-banner">
                    <span class="spinner-pulse"></span>
                    <span>⏳ <strong>[Planning Gate]</strong> 구현 계획서를 확인하신 후 아래 [승인하고 진행]을 클릭해 주세요.</span>
                </div>
            `;
        }

        // 📋 5. 아티팩트 카드 (Artifact Card - Antigravity Style)
        if (res.artifacts && res.artifacts.length > 0) {
            res.artifacts.forEach(art => {
                registerArtifact(art);
                html += createArtifactCardHtml(art);
            });
        }

        // 📝 6. Live Multi-File Diff (Windsurf Cascade Style)
        if (res.file_diffs && res.file_diffs.length > 0 && !res.is_waiting_approval) {
            activeSessionDiffs = res.file_diffs;
            html += createMultiFileDiffHtml(res.file_diffs);
        } else if (res.code_diff && !res.is_waiting_approval) {
            html += `
                <div style="margin-top: 8px;">
                    <strong>[생성된 코드 Diff (${escapeHtml(res.code_filename || 'source.py')})]</strong>
                    <pre><code>${escapeHtml(res.code_diff)}</code></pre>
                </div>
            `;
        }

        // 🧪 7. Sandbox Terminal Log
        if (res.terminal_log && !res.is_waiting_approval) {
            html += `
                <div class="accordion-block" style="margin-top:6px;">
                    <div class="accordion-header" onclick="this.nextElementSibling.classList.toggle('collapsed')">
                        <span>🧪 샌드박스 실행 로그</span>
                        <span style="font-size:0.7rem; color:var(--success);">▼</span>
                    </div>
                    <div class="accordion-body collapsed">
                        <pre style="margin:0;">${escapeHtml(res.terminal_log)}</pre>
                    </div>
                </div>
            `;
        }

        responseBox.innerHTML = html;
        chatMessages.appendChild(responseBox);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // ==========================================
    // 10. Multi-File Diff HTML 빌더
    // ==========================================
    function createMultiFileDiffHtml(diffs) {
        return `
            <div class="diff-container">
                <div class="diff-main-header">
                    <div class="diff-main-title">
                        <span>📝 Live Multi-File Diffs (${diffs.length}개 파일 변경)</span>
                    </div>
                    <div class="diff-global-actions">
                        <button class="btn-diff-all-accept" onclick="window.acceptAllDiffs()">✓ 모두 수락</button>
                        <button class="btn-diff-all-rollback" onclick="window.rollbackAllDiffs()">↺ 전체 롤백</button>
                    </div>
                </div>
                ${diffs.map((d, idx) => `
                    <div class="diff-file-card" id="diff-card-${escapeJs(d.path.replace(/[/\\.]/g, '_'))}">
                        <div class="diff-file-header">
                            <div class="diff-file-info">
                                <span>📄 ${escapeHtml(d.filename)}</span>
                                <span class="diff-stats">
                                    <span class="stat-add">+${d.additions || 0}</span>
                                    <span class="stat-del">-${d.deletions || 0}</span>
                                </span>
                            </div>
                            <div class="diff-file-actions" id="diff-actions-${escapeJs(d.path.replace(/[/\\.]/g, '_'))}">
                                <button class="btn-diff-action compare" onclick="window.openDiffViewer('${escapeJs(d.path)}', ${idx})">
                                    🔍 Diff 비교
                                </button>
                                <button class="btn-diff-action accept" onclick="window.acceptSingleDiff('${escapeJs(d.path)}', ${idx})">
                                    ✓ Accept
                                </button>
                                <button class="btn-diff-action reject" onclick="window.rejectSingleDiff('${escapeJs(d.path)}', ${idx})">
                                    ✕ Reject
                                </button>
                            </div>
                        </div>
                        <pre class="diff-code-view"><code>${escapeHtml(d.diff_text)}</code></pre>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // ==========================================
    // 11. 아티팩트 카드 및 드로어 관리
    // ==========================================
    function createArtifactCardHtml(art) {
        const tagClass = art.type || 'spec';
        const tagLabel = art.type === 'plan' ? '계획서' : art.type === 'walkthrough' ? '워크스루' : '명세서';
        const cardId = 'art-' + Math.random().toString(36).substr(2, 9);

        return `
            <div class="artifact-card" id="${cardId}">
                <div class="artifact-card-header">
                    <span class="artifact-tag ${tagClass}">${tagLabel}</span>
                    <span class="artifact-filename">${escapeHtml(art.filename)}</span>
                </div>
                <div class="artifact-summary">${escapeHtml(art.summary || '상세 작업 아티팩트 문서입니다.')}</div>
                <div class="artifact-actions" id="actions-${cardId}">
                    <button class="btn-artifact-view" onclick="window.openArtifactFile('${escapeJs(art.path || art.filename)}')">
                        📄 에디터에서 열기 ↗
                    </button>
                    ${art.request_feedback ? `
                    <button class="btn-artifact-approve" onclick="window.approvePlan('${escapeJs(art.path || art.filename)}', '${cardId}')">
                        ✓ 승인하고 진행 (Proceed)
                    </button>
                    <button class="btn-artifact-feedback" onclick="window.requestPlanFeedback('${escapeJs(art.path || art.filename)}')">
                        ✎ 피드백 입력
                    </button>
                    ` : ''}
                </div>
            </div>
        `;
    }

    function registerArtifact(art) {
        const existingIdx = sessionArtifacts.findIndex(a => a.filename === art.filename || a.path === art.path);
        if (existingIdx >= 0) {
            sessionArtifacts[existingIdx] = art;
        } else {
            sessionArtifacts.push(art);
        }
        updateDrawerList();
    }

    function updateDrawerList() {
        if (!artifactsCount || !drawerArtifactsList) return;
        artifactsCount.textContent = sessionArtifacts.length;

        if (sessionArtifacts.length === 0) {
            drawerArtifactsList.innerHTML = '<div class="drawer-empty">아직 생성된 아티팩트가 없습니다.</div>';
            return;
        }

        drawerArtifactsList.innerHTML = sessionArtifacts.map(art => `
            <div class="drawer-item">
                <div class="drawer-item-title">
                    <span>📄 ${escapeHtml(art.filename)}</span>
                    <span class="artifact-tag ${art.type || 'spec'}">${art.type || 'spec'}</span>
                </div>
                <div class="drawer-item-summary">${escapeHtml(art.summary || art.title || '')}</div>
                <div class="drawer-item-actions">
                    <button class="btn-drawer-open" onclick="window.openArtifactFile('${escapeJs(art.path || art.filename)}')">
                        에디터 열기 ↗
                    </button>
                </div>
            </div>
        `).join('');
    }

    // ==========================================
    // 12. 세션 / Mem0 / Graphify / gstack 렌더러
    // ==========================================
    function renderSessionsList(sessions) {
        if (!drawerSessionsList) return;
        if (!sessions || sessions.length === 0) {
            drawerSessionsList.innerHTML = '<div class="drawer-empty">저장된 세션이 없습니다.</div>';
            return;
        }

        drawerSessionsList.innerHTML = sessions.map(s => `
            <div class="session-item">
                <div class="session-item-header">
                    <span class="session-title" title="${escapeHtml(s.title)}">💬 ${escapeHtml(s.title || '새 세션')}</span>
                    <span class="session-time">${s.updated_at ? s.updated_at.slice(5, 16).replace('T', ' ') : ''}</span>
                </div>
                <div class="session-item-actions">
                    <button class="btn-session-load" onclick="window.loadSession('${escapeJs(s.id)}')">이어하기 ↗</button>
                    <button class="btn-session-del" onclick="window.deleteSession('${escapeJs(s.id)}')">삭제</button>
                </div>
            </div>
        `).join('');
    }

    function renderMem0List(memories) {
        if (!drawerMem0List) return;
        if (!memories || memories.length === 0) {
            drawerMem0List.innerHTML = '<div class="drawer-empty">저장된 기억 프로필이 없습니다.</div>';
            return;
        }

        drawerMem0List.innerHTML = memories.map(m => `
            <div class="mem0-item">
                <div class="mem0-item-header">
                    <span class="mem0-key">📌 ${escapeHtml(m.key)}</span>
                    <span class="mem0-category">${escapeHtml(m.category)}</span>
                </div>
                <div class="mem0-val">${escapeHtml(m.value)}</div>
            </div>
        `).join('');
    }

    function renderGraphifyStats(data) {
        if (!drawerGraphifyList) return;
        const stats = data.stats || {};
        const nodes = data.nodes || [];

        let html = `
            <div class="graphify-stats-box">
                <div class="graphify-stat-item"><span>인덱싱 파일:</span><strong>${stats.files_indexed || 0}개</strong></div>
                <div class="graphify-stat-item"><span>AST 심볼:</span><strong>${stats.symbols_indexed || 0}개</strong></div>
                <div class="graphify-stat-item"><span>그래프 노드:</span><strong>${stats.total_nodes || 0}개</strong></div>
                <div class="graphify-stat-item"><span>호출 엣지:</span><strong>${stats.total_edges || 0}개</strong></div>
            </div>
            <div style="font-size:0.75rem; font-weight:700; color:#e040fb; margin-bottom:6px;">최근 파싱된 AST 심볼 목록:</div>
        `;

        html += nodes.slice(0, 20).map(n => `
            <div class="graphify-node-item">
                <span>${escapeHtml(n.label)}</span>
                <span class="graphify-node-type ${n.type}">${n.type}</span>
            </div>
        `).join('');

        drawerGraphifyList.innerHTML = html;
    }

    function renderGstackPlugins(data) {
        if (!drawerPluginsList) return;
        const personas = data.personas || [];
        const workflows = data.workflows || [];

        let html = `
            <div class="plugin-section-title">🧭 전문가 페르소나 (Personas - ${personas.length}개)</div>
            <div class="persona-grid">
                ${personas.map(p => `
                    <div class="persona-card" onclick="window.insertPersona('${escapeJs(p.id)}')">
                        <div class="persona-card-header">
                            <span>${p.icon || '🧭'}</span>
                            <span style="color:#00e5ff;">${escapeHtml(p.id)}</span>
                        </div>
                        <div style="font-size:0.72rem; font-weight:700; color:#ffffff;">${escapeHtml(p.name)}</div>
                        <div class="persona-card-desc">${escapeHtml(p.desc)}</div>
                    </div>
                `).join('')}
            </div>

            <div class="plugin-section-title">⚡ 라이프사이클 워크플로우 (Workflows - ${workflows.length}개)</div>
            <div>
                ${workflows.map(w => `
                    <div class="workflow-card" onclick="window.insertWorkflow('${escapeJs(w.command)}')">
                        <span class="workflow-cmd">${escapeHtml(w.command)}</span>
                        <span style="color:var(--text-muted);">${escapeHtml(w.name)}</span>
                    </div>
                `).join('')}
            </div>
        `;

        drawerPluginsList.innerHTML = html;
    }

    function loadSessionData(data) {
        if (sessionsDrawer) sessionsDrawer.classList.remove('active');
        chatMessages.innerHTML = `
            <div class="message system-msg">
                <strong>[세션 복원]</strong> '${escapeHtml(data.session.title)}' 세션이 복원되었습니다.
            </div>
        `;
        if (data.messages) {
            data.messages.forEach(m => {
                appendMessage(m.role, m.content);
            });
        }
        if (data.artifacts) {
            sessionArtifacts = data.artifacts;
            updateDrawerList();
        }
    }

    function updateDiffStatusInUi(filePath, status) {
        const idKey = filePath.replace(/[/\\.]/g, '_');
        const actionsEl = document.getElementById(`diff-actions-${idKey}`);
        if (actionsEl) {
            const badgeClass = status === 'accepted' ? 'accepted' : 'rolled_back';
            const badgeLabel = status === 'accepted' ? '✓ Accepted' : '↺ Rolled Back';
            actionsEl.innerHTML = `<span class="diff-badge-status ${badgeClass}">${badgeLabel}</span>`;
        }
    }

    // ==========================================
    // 13. 전역 인터랙션 바인딩 함수
    // ==========================================
    window.insertPersona = function (personaId) {
        chatInput.value = `${personaId} ` + chatInput.value.replace(/@[a-zA-Z0-9_\-]+/g, '').trim();
        if (pluginsDrawer) pluginsDrawer.classList.remove('active');
        chatInput.focus();
    };

    window.insertWorkflow = function (command) {
        chatInput.value = `${command} ` + chatInput.value.replace(/\/[a-zA-Z0-9_\-]+/g, '').trim();
        if (pluginsDrawer) pluginsDrawer.classList.remove('active');
        chatInput.focus();
    };

    window.openArtifactFile = function (filePath) {
        vscode.postMessage({ command: 'openFile', filePath: filePath });
    };

    window.openDiffViewer = function (filePath, idx) {
        const d = activeSessionDiffs[idx];
        if (!d) return;
        vscode.postMessage({
            command: 'openDiff',
            filePath: d.path,
            originalContent: d.original_content,
            modifiedContent: d.modified_content
        });
    };

    window.acceptSingleDiff = function (filePath, idx) {
        const d = activeSessionDiffs[idx];
        if (!d) return;
        vscode.postMessage({
            command: 'acceptDiff',
            filePath: d.path,
            modifiedContent: d.modified_content,
            diffId: d.id
        });
    };

    window.rejectSingleDiff = function (filePath, idx) {
        const d = activeSessionDiffs[idx];
        if (!d) return;
        vscode.postMessage({
            command: 'rollbackDiff',
            filePath: d.path,
            originalContent: d.original_content,
            diffId: d.id
        });
    };

    window.acceptAllDiffs = function () {
        activeSessionDiffs.forEach((d, idx) => {
            window.acceptSingleDiff(d.path, idx);
        });
    };

    window.rollbackAllDiffs = function () {
        activeSessionDiffs.forEach((d, idx) => {
            window.rejectSingleDiff(d.path, idx);
        });
    };

    window.loadSession = function (sessionId) {
        vscode.postMessage({ command: 'loadSession', sessionId: sessionId });
    };

    window.deleteSession = function (sessionId) {
        vscode.postMessage({ command: 'deleteSession', sessionId: sessionId });
        setTimeout(() => {
            vscode.postMessage({ command: 'listSessions' });
        }, 300);
    };

    window.approvePlan = function (planPath, cardId) {
        const actionsEl = document.getElementById(`actions-${cardId}`);
        if (actionsEl) {
            actionsEl.innerHTML = `
                <button class="btn-artifact-view" onclick="window.openArtifactFile('${escapeJs(planPath)}')">
                    📄 에디터에서 열기 ↗
                </button>
                <span class="artifact-approved-badge">✓ 계획 승인됨 (Approved)</span>
            `;
        }

        appendMessage('user', `[계획 승인] ${planPath} 구현 계획을 승인합니다. 실제 코드 변경 및 실행을 진행해 주세요.`);
        appendMessage('system', '사용자 승인이 확인되었습니다. <strong>자율 실행 루프(Execution Loop)</strong>로 전환하여 코드 생성 및 Multi-File Diff를 시작합니다...');

        vscode.postMessage({
            command: 'sendVibe',
            intent: `이전 생성된 계획서(${planPath})가 사용자에 의해 공식 승인되었습니다. 계획에 따라 소스코드 변경 및 상세명세서 작성을 실행 완료하세요.`,
            mode: 'direct',
            modelId: modelSelect.value
        });
    };

    window.requestPlanFeedback = function (planPath) {
        chatInput.value = `[계획서 수정 피드백: ${planPath}] `;
        chatInput.focus();
    };

    function escapeHtml(text) {
        if (!text) return '';
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function escapeJs(text) {
        if (!text) return '';
        return String(text).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    }
}());
