(function () {
    const vscode = acquireVsCodeApi();
    
    // UI Elements
    const authOverlay = document.getElementById('auth-overlay');
    const emailSection = document.getElementById('email-section');
    const otpSection = document.getElementById('otp-section');
    const authEmail = document.getElementById('auth-email');
    const authOtp = document.getElementById('auth-otp');
    const btnSendOtp = document.getElementById('btn-send-otp');
    const btnVerifyOtp = document.getElementById('btn-verify-otp');
    const btnBackEmail = document.getElementById('btn-back-email');
    const authMessage = document.getElementById('auth-message');
    
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const btnMic = document.getElementById('btn-mic');
    const btnSend = document.getElementById('btn-send');
    const modelSelect = document.getElementById('model-select');

    let currentEmail = '';
    let isRecording = false;

    // 1. 이메일 OTP 전송 요청
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

    // 2. OTP 검증 요청
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

    // 이전 단계로 돌아가기
    btnBackEmail.addEventListener('click', () => {
        otpSection.classList.remove('active');
        emailSection.classList.add('active');
        authOtp.value = '';
        authMessage.textContent = '';
    });

    // 3. 메시지 발송
    btnSend.addEventListener('click', sendUserMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendUserMessage();
        }
    });

    function sendUserMessage() {
        const intent = chatInput.value.trim();
        if (!intent) return;

        appendMessage('user', intent);
        chatInput.value = '';
        
        const modelId = modelSelect.value;
        appendMessage('system', '에이전트가 지시 사항을 분석하고 있습니다...');

        vscode.postMessage({
            command: 'sendVibe',
            intent: intent,
            modelId: modelId,
            targetFile: "auth_service.py"
        });
    }

    // 🎤 4. 음성 인식 (STT) 실구현 및 핸들러
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
                    reader.onloadend = () => {
                        const base64Audio = reader.result.split(',')[1];
                        vscode.postMessage({
                            command: 'audioData',
                            data: base64Audio
                        });
                    };
                    reader.readAsDataURL(audioBlob);
                    
                    // 마이크 스트림 닫기
                    stream.getTracks().forEach(track => track.stop());
                });

                mediaRecorder.start();
                isRecording = true;
                btnMic.classList.add('recording');
                btnMic.title = '녹음 중... (다시 클릭하여 중지)';
                
            } catch (err) {
                appendMessage('system', `[오류] 마이크 접근 실패: ${err.message}`);
                isRecording = false;
                btnMic.classList.remove('recording');
            }
        } else {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
            isRecording = false;
            btnMic.classList.remove('recording');
            btnMic.title = '음성 인식 지시 (STT)';
        }
    });

    // 5. 호스트(extension.js) 응답 리스너
    window.addEventListener('message', event => {
        const message = event.data;
        switch (message.command) {
            case 'sendOtpResponse':
                if (message.success) {
                    authMessage.textContent = '';
                    emailSection.classList.remove('active');
                    otpSection.classList.add('active');
                } else {
                    showAuthError(message.error || 'OTP 전송에 실패했습니다.');
                }
                break;
            case 'verifyOtpResponse':
                if (message.success) {
                    // 인증 성공 ➔ 오버레이 제거 및 메인화면 로드
                    authOverlay.classList.remove('active');
                    appendMessage('system', `[인증 완료] 사내 메일 계정(${currentEmail})으로 성공적으로 로그인하였습니다.`);
                } else {
                    showAuthError(message.error || '잘못된 보안코드이거나 만료되었습니다.');
                }
                break;
            case 'sendVibeResponse':
                // 대기 메시지 제거
                removeSystemLoadingMessage();
                
                if (message.success) {
                    const res = message.data;
                    appendAgentResponse(res);
                } else {
                    appendMessage('agent', `[에러 발생] Vibe 코드 생성 실패: ${message.error}`);
                }
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

    function appendAgentResponse(res) {
        const responseBox = document.createElement('div');
        responseBox.classList.add('message', 'agent-msg');

        let html = '';
        
        // 1. Thinking Process
        if (res.thinking && res.thinking.length > 0) {
            html += '<div class="thinking-block"><strong>[사고 과정]</strong><br>';
            res.thinking.forEach(step => {
                html += `• ${step}<br>`;
            });
            html += '</div>';
        }

        // 2. Generated Diff
        if (res.code_diff) {
            html += `<strong>[생성된 코드 Diff (${res.code_filename})]</strong><pre><code>${escapeHtml(res.code_diff)}</code></pre>`;
        }

        // 3. Sandbox Terminal Log
        if (res.terminal_log) {
            html += `<strong>[샌드박스 결과]</strong><pre>${escapeHtml(res.terminal_log)}</pre>`;
        }

        responseBox.innerHTML = html;
        chatMessages.appendChild(responseBox);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}());
