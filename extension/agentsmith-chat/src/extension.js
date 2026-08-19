const vscode = require('vscode');
const http = require('http');
const path = require('path');
const fs = require('fs');
const os = require('os');

function activate(context) {
    const provider = new AgentSmithChatViewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            'agentsmith-chat-view',
            provider
        )
    );
}

class AgentSmithChatViewProvider {
    constructor(extensionUri) {
        this._extensionUri = extensionUri;
        this._currentSessionId = null;
    }

    resolveWebviewView(webviewView, context, _token) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Webview 메시지 수신 및 백엔드 REST API 중계
        webviewView.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'sendOtp':
                    this._callBackend('/api/auth/otp/send', 'POST', { email: message.email }, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'sendOtpResponse',
                            success: !err,
                            data: data,
                            error: err ? err.message : null
                        });
                    });
                    break;
                case 'verifyOtp':
                    this._callBackend('/api/auth/otp/verify', 'POST', { email: message.email, otp_code: message.otpCode }, (err, data) => {
                        webviewView.webview.postMessage({
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
                        mode: message.mode || "planning",
                        session_id: this._currentSessionId,
                        target_file: message.targetFile || "auth_service.py" 
                    }, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'sendVibeResponse',
                            success: !err,
                            data: data,
                            error: err ? err.message : null
                        });
                    });
                    break;
                case 'openFile':
                    this._openFileInEditor(message.filePath);
                    break;
                case 'openDiff':
                    this._openNativeDiff(message.filePath, message.originalContent, message.modifiedContent);
                    break;
                case 'acceptDiff':
                    this._applyDiffToFile(message.filePath, message.modifiedContent, message.diffId, webviewView);
                    break;
                case 'rollbackDiff':
                    this._rollbackDiffFile(message.filePath, message.originalContent, message.diffId, webviewView);
                    break;
                case 'scanArtifacts':
                    this._scanWorkspaceArtifacts(webviewView);
                    break;
                case 'listSessions':
                    this._callBackend('/api/sessions', 'GET', null, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'sessionsListResponse',
                            success: !err,
                            sessions: data ? data.sessions : []
                        });
                    });
                    break;
                case 'loadSession':
                    this._currentSessionId = message.sessionId;
                    this._callBackend(`/api/sessions/${message.sessionId}`, 'GET', null, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'sessionLoadedResponse',
                            success: !err,
                            data: data
                        });
                    });
                    break;
                case 'deleteSession':
                    this._callBackend(`/api/sessions/${message.sessionId}`, 'DELETE', null, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'sessionDeletedResponse',
                            success: !err
                        });
                    });
                    break;
                case 'newChat':
                    this._callBackend('/api/sessions/new', 'POST', { title: "새 세션" }, (err, data) => {
                        if (data) this._currentSessionId = data.id;
                        this._scanWorkspaceArtifacts(webviewView);
                    });
                    break;
                case 'audioData':
                    this._callWhisperSTT(message.data, (err, text) => {
                        webviewView.webview.postMessage({
                            command: 'sttResponse',
                            success: !err,
                            text: text,
                            error: err ? err.message : null
                        });
                    });
                    break;
            }
        });
    }

    _openFileInEditor(targetPath) {
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
                vscode.window.showTextDocument(doc, { preview: false });
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

    _applyDiffToFile(filePath, modifiedContent, diffId, webviewView) {
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

            webviewView.webview.postMessage({
                command: 'diffAppliedResponse',
                filePath: filePath,
                status: 'accepted'
            });
        } catch (e) {
            vscode.window.showErrorMessage(`파일 저장 실패: ${e.message}`);
        }
    }

    _rollbackDiffFile(filePath, originalContent, diffId, webviewView) {
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

            webviewView.webview.postMessage({
                command: 'diffRolledBackResponse',
                filePath: filePath,
                status: 'rolled_back'
            });
        } catch (e) {
            vscode.window.showErrorMessage(`롤백 실패: ${e.message}`);
        }
    }

    _scanWorkspaceArtifacts(webviewView) {
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

        webviewView.webview.postMessage({
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
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.js'));
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.css'));
        const htmlUri = vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.html');

        let htmlContent = '';
        try {
            htmlContent = fs.readFileSync(htmlUri.fsPath, 'utf8');
        } catch (e) {
            htmlContent = '<html><body><h3>Error loading Chat UI</h3></body></html>';
        }

        htmlContent = htmlContent.replace('${styleUri}', styleUri);
        htmlContent = htmlContent.replace('${scriptUri}', scriptUri);

        return htmlContent;
    }
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
