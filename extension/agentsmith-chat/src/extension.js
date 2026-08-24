const vscode = require('vscode');
const http = require('http');
const path = require('path');
const fs = require('fs');
const os = require('os');

function activate(context) {
    console.log('[Agent Smith] Center Studio Extension Activated.');

    // 1. 명령어 등록 (중앙 에디터 스튜디오 열기)
    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openEditorPanel', () => {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openChat', () => {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        })
    );

    // 2. 상태표시줄(Status Bar)에 원클릭 Studio 열기 버튼 등록
    try {
        const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
        statusBarItem.command = 'agentsmith.openEditorPanel';
        statusBarItem.text = '$(sparkle) Agent Smith Studio';
        statusBarItem.tooltip = 'Agent Smith AI Studio 열기 (Ctrl+Alt+A)';
        statusBarItem.show();
        context.subscriptions.push(statusBarItem);
    } catch (e) {
        console.error('[Agent Smith] StatusBarItem 생성 실패:', e);
    }

    // 3. 데스크톱 앱 시작 시:
    //   - 중앙 에디터 영역(Welcome 위치)에 Agent Smith Studio 자동 실행
    //   - 좌측 사이드바는 파일 탐색기(Explorer)로 전환하여 3창 분리 레이아웃 완성
    setTimeout(() => {
        try {
            // 중앙 Welcome 위치에 Studio 실행
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);

            // 좌측 사이드바를 파일 탐색기로 확실히 포커스
            vscode.commands.executeCommand('workbench.view.explorer');
        } catch (e) {
            console.error('[Agent Smith] 중앙 에디터 패널 자동 기동 실패:', e);
        }
    }, 250);
}

class AgentSmithChatViewProvider {
    constructor(extensionUri) {
        this._extensionUri = extensionUri;
        this._currentSessionId = null;
    }

    /**
     * Welcome 탭 위치(중앙 에디터 영역 ViewColumn.One)에 Agent Smith Studio 패널 생성 또는 표시.
     */
    static createOrShowEditorPanel(extensionUri) {
        // 이미 열린 패널이 있으면 해당 패널을 앞으로 가져옴
        if (AgentSmithChatViewProvider._currentEditorPanel) {
            AgentSmithChatViewProvider._currentEditorPanel.reveal(vscode.ViewColumn.One);
            return;
        }

        // 중앙 에디터 영역(ViewColumn.One = Welcome 위치)에 새 WebviewPanel 생성
        const panel = vscode.window.createWebviewPanel(
            'agentsmithStudioPanel',
            'Agent Smith Studio',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        // 탭 헤더에 Trinity Air 브랜드 로고 아이콘 지정
        panel.iconPath = vscode.Uri.joinPath(extensionUri, 'media', 'logo.svg');

        // HTML 렌더링
        const provider = new AgentSmithChatViewProvider(extensionUri);
        panel.webview.html = provider._getHtmlForWebview(panel.webview);

        // 메시지 핸들러 등록
        panel.webview.onDidReceiveMessage(message => {
            provider._handleWebviewMessage(message, panel.webview);
        });

        // 패널 닫힘 시 정리
        panel.onDidDispose(() => {
            AgentSmithChatViewProvider._currentEditorPanel = undefined;
        });

        AgentSmithChatViewProvider._currentEditorPanel = panel;
    }

    /**
     * 중앙 에디터 패널에서 오는 메시지를 처리하는 핸들러.
     */
    _handleWebviewMessage(message, webview) {
        switch (message.command) {
            case 'sendOtp':
                this._callBackend('/api/auth/otp/send', 'POST', { email: message.email }, (err, data) => {
                    webview.postMessage({
                        command: 'sendOtpResponse',
                        success: !err,
                        data: data,
                        error: err ? err.message : null
                    });
                });
                break;
            case 'verifyOtp':
                this._callBackend('/api/auth/otp/verify', 'POST', { email: message.email, otp_code: message.otpCode }, (err, data) => {
                    webview.postMessage({
                        command: 'verifyOtpResponse',
                        success: !err,
                        data: data,
                        error: err ? err.message : null
                    });
                });
                break;
            case 'sendVibe':
                this._callBackend('/api/vibe/generate', 'POST', {
                    intent: message.intent,
                    model_id: message.modelId,
                    mode: message.mode || 'planning',
                    session_id: this._currentSessionId,
                    target_file: message.targetFile || 'auth_service.py'
                }, (err, data) => {
                    webview.postMessage({
                        command: 'sendVibeResponse',
                        success: !err,
                        data: data,
                        error: err ? err.message : null
                    });
                });
                break;
            case 'openFile':
                // 3창 워크플로우: Studio(중앙 ViewColumn.One)를 유지하면서 우측 분할(ViewColumn.Beside)로 파일 오픈
                this._openFileInEditor(message.filePath || message.path, true);
                break;
            case 'openDiff':
                this._openNativeDiff(message.filePath || message.path, message.originalContent, message.modifiedContent);
                break;
            case 'acceptDiff':
                if (message.modifiedContent) {
                    this._applyDiffToFile(message.filePath || message.file, message.modifiedContent, message.diffId, webview);
                } else {
                    vscode.window.showInformationMessage(`[Agent Smith] ${message.file || message.filePath || '파일'}의 변경사항이 수락되어 작업공간에 반영되었습니다.`);
                }
                break;
            case 'rollbackDiff':
                if (message.originalContent) {
                    this._rollbackDiffFile(message.filePath || message.file, message.originalContent, message.diffId, webview);
                } else {
                    vscode.window.showInformationMessage(`[Agent Smith] ${message.file || message.filePath || '파일'}의 변경사항이 원본으로 롤백되었습니다.`);
                }
                break;
            case 'scanArtifacts':
                this._scanWorkspaceArtifacts(webview);
                break;
            case 'listSessions':
                this._callBackend('/api/sessions', 'GET', null, (err, data) => {
                    webview.postMessage({
                        command: 'sessionsListResponse',
                        success: !err,
                        sessions: data ? data.sessions : []
                    });
                });
                break;
            case 'loadSession':
                this._currentSessionId = message.sessionId;
                this._callBackend(`/api/sessions/${message.sessionId}`, 'GET', null, (err, data) => {
                    webview.postMessage({
                        command: 'sessionLoadedResponse',
                        success: !err,
                        data: data
                    });
                });
                break;
            case 'deleteSession':
                this._callBackend(`/api/sessions/${message.sessionId}`, 'DELETE', null, (err, data) => {
                    webview.postMessage({
                        command: 'sessionDeletedResponse',
                        success: !err
                    });
                });
                break;
            case 'newChat':
                this._callBackend('/api/sessions/new', 'POST', { title: '새 세션' }, (err, data) => {
                    if (data) this._currentSessionId = data.id;
                    this._scanWorkspaceArtifacts(webview);
                });
                break;
            case 'audioData':
                this._callWhisperSTT(message.data, (err, text) => {
                    webview.postMessage({
                        command: 'sttResponse',
                        success: !err,
                        text: text,
                        error: err ? err.message : null
                    });
                });
                break;
        }
    }

    _openFileInEditor(targetPath, openBeside = true) {
        if (!targetPath) return;

        let fullPath = targetPath;
        if (!path.isAbsolute(targetPath)) {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (workspaceFolders && workspaceFolders.length > 0) {
                fullPath = path.join(workspaceFolders[0].uri.fsPath, targetPath);
            }
        }

        if (fs.existsSync(fullPath)) {
            const uri = vscode.Uri.file(fullPath);
            vscode.workspace.openTextDocument(uri).then(doc => {
                // openBeside=true 이면 ViewColumn.Beside(우측 분할)로 열어 3창 레이아웃 유지
                const options = openBeside
                    ? { viewColumn: vscode.ViewColumn.Beside, preview: false }
                    : { preview: false };
                vscode.window.showTextDocument(doc, options);
            }, err => {
                vscode.window.showErrorMessage(`문서를 열 수 없습니다: ${err.message}`);
            });
        } else {
            vscode.window.showWarningMessage(`파일을 찾을 수 없습니다: ${targetPath}`);
        }
    }

    _openNativeDiff(filePath, originalContent, modifiedContent) {
        try {
            const tempDir = path.join(os.tmpdir(), 'agentsmith_diffs');
            fs.mkdirSync(tempDir, { recursive: true });

            const baseName = path.basename(filePath);
            const origPath = path.join(tempDir, `original_${baseName}`);
            const modPath = path.join(tempDir, `modified_${baseName}`);

            fs.writeFileSync(origPath, originalContent || '', 'utf8');
            fs.writeFileSync(modPath, modifiedContent || '', 'utf8');

            const origUri = vscode.Uri.file(origPath);
            const modUri = vscode.Uri.file(modPath);

            vscode.commands.executeCommand(
                'vscode.diff',
                origUri,
                modUri,
                `${baseName} (Original ↔ Proposed)`
            );
        } catch (e) {
            vscode.window.showErrorMessage(`Diff 뷰어 실행 실패: ${e.message}`);
        }
    }

    _applyDiffToFile(filePath, modifiedContent, diffId, webview) {
        try {
            let fullPath = filePath;
            if (!path.isAbsolute(filePath)) {
                const workspaceFolders = vscode.workspace.workspaceFolders;
                if (workspaceFolders && workspaceFolders.length > 0) {
                    fullPath = path.join(workspaceFolders[0].uri.fsPath, filePath);
                }
            }

            fs.mkdirSync(path.dirname(fullPath), { recursive: true });
            fs.writeFileSync(fullPath, modifiedContent, 'utf8');

            vscode.window.showInformationMessage(`[Accept 완료] ${path.basename(filePath)} 파일이 저장되었습니다.`);

            // 백엔드 상태 동기화
            this._callBackend('/api/diff/apply', 'POST', { diff_id: diffId, file_path: filePath, content: modifiedContent }, () => {});

            webview.postMessage({
                command: 'diffAppliedResponse',
                filePath: filePath,
                status: 'accepted'
            });
        } catch (e) {
            vscode.window.showErrorMessage(`파일 저장 실패: ${e.message}`);
        }
    }

    _rollbackDiffFile(filePath, originalContent, diffId, webview) {
        try {
            let fullPath = filePath;
            if (!path.isAbsolute(filePath)) {
                const workspaceFolders = vscode.workspace.workspaceFolders;
                if (workspaceFolders && workspaceFolders.length > 0) {
                    fullPath = path.join(workspaceFolders[0].uri.fsPath, filePath);
                }
            }

            if (originalContent) {
                fs.writeFileSync(fullPath, originalContent, 'utf8');
            }

            vscode.window.showInformationMessage(`[Rollback 완료] ${path.basename(filePath)} 파일이 원본 상태로 복원되었습니다.`);

            // 백엔드 상태 동기화
            this._callBackend('/api/diff/rollback', 'POST', { diff_id: diffId, file_path: filePath, content: originalContent }, () => {});

            webview.postMessage({
                command: 'diffRolledBackResponse',
                filePath: filePath,
                status: 'rolled_back'
            });
        } catch (e) {
            vscode.window.showErrorMessage(`롤백 실패: ${e.message}`);
        }
    }

    _scanWorkspaceArtifacts(webview) {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) return;

        const rootPath = workspaceFolders[0].uri.fsPath;
        const scanDirs = [
            path.join(rootPath, 'coding-agent', 'docs', 'plans'),
            path.join(rootPath, 'coding-agent', 'docs', 'specs'),
            path.join(rootPath, 'docs', 'plans'),
            path.join(rootPath, 'docs', 'specs')
        ];

        const artifacts = [];

        scanDirs.forEach(dir => {
            if (fs.existsSync(dir)) {
                try {
                    const files = fs.readdirSync(dir);
                    files.filter(f => f.endsWith('.md')).forEach(file => {
                        const filePath = path.join(dir, file);
                        const relPath = path.relative(rootPath, filePath);
                        const isPlan = file.includes('plan');
                        const isSpec = file.includes('spec');

                        artifacts.push({
                            title: file,
                            filename: file,
                            path: relPath,
                            type: isPlan ? 'plan' : isSpec ? 'spec' : 'walkthrough',
                            summary: isPlan ? '작업 계획서 아티팩트' : '상세 명세서 아티팩트',
                            request_feedback: isPlan
                        });
                    });
                } catch (e) {
                    console.error('Error scanning artifacts in dir:', dir, e);
                }
            }
        });

        artifacts.reverse();

        webview.postMessage({
            command: 'artifactsScanned',
            artifacts: artifacts.slice(0, 15)
        });
    }

    _callWhisperSTT(base64Audio, callback) {
        const postData = JSON.stringify({ file_base64: base64Audio });

        const options = {
            hostname: '127.0.0.1',
            port: 5000,
            path: '/api/audio/transcriptions',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        const req = http.request(options, (res) => {
            let resBody = '';
            res.setEncoding('utf8');
            res.on('data', (chunk) => resBody += chunk);
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(resBody);
                    if (res.statusCode >= 400) {
                        callback(new Error(parsed.detail || `Server error: ${res.statusCode}`), null);
                    } else {
                        callback(null, parsed.text);
                    }
                } catch (e) {
                    callback(new Error('Response parsing failure'), null);
                }
            });
        });

        req.on('error', (e) => {
            callback(new Error(`Connection failure: ${e.message}`), null);
        });

        req.write(postData);
        req.end();
    }

    _callBackend(apiPath, method, payload, callback) {
        const postData = payload ? JSON.stringify(payload) : '';
        const options = {
            hostname: '127.0.0.1',
            port: 5000,
            path: apiPath,
            method: method || 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (postData) {
            options.headers['Content-Length'] = Buffer.byteLength(postData);
        }

        const req = http.request(options, (res) => {
            let body = '';
            res.setEncoding('utf8');
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(body);
                    if (res.statusCode >= 400) {
                        callback(new Error(parsed.detail || `Server error: ${res.statusCode}`), null);
                    } else {
                        callback(null, parsed);
                    }
                } catch (e) {
                    callback(null, body);
                }
            });
        });

        req.on('error', (e) => {
            callback(new Error(`Connection failure: ${e.message}`), null);
        });

        if (postData) {
            req.write(postData);
        }
        req.end();
    }

    _getHtmlForWebview(webview) {
        const mediaPath = path.join(this._extensionUri.fsPath, 'media');
        const indexPath = path.join(mediaPath, 'index.html');

        let htmlContent = '';
        try {
            htmlContent = fs.readFileSync(indexPath, 'utf8');
        } catch (e) {
            htmlContent = '<html><body><h3>Error loading Agent Smith Studio</h3></body></html>';
        }

        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'style.css'));
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'app.js'));

        htmlContent = htmlContent.replace('href="style.css"', `href="${styleUri}"`);
        htmlContent = htmlContent.replace('src="app.js"', `src="${scriptUri}"`);

        return htmlContent;
    }
}

// 정적 멤버: 현재 열린 에디터 패널 참조 (싱글톤)
AgentSmithChatViewProvider._currentEditorPanel = undefined;

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
