const vscode = require('vscode');
const http = require('http');

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
                    this._callBackend('/api/auth/otp/send', { email: message.email }, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'sendOtpResponse',
                            success: !err,
                            data: data,
                            error: err ? err.message : null
                        });
                    });
                    break;
                case 'verifyOtp':
                    this._callBackend('/api/auth/otp/verify', { email: message.email, otp_code: message.otpCode }, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'verifyOtpResponse',
                            success: !err,
                            data: data,
                            error: err ? err.message : null
                        });
                    });
                    break;
                case 'sendVibe':
                    this._callBackend('/api/vibe/generate', { intent: message.intent, model_id: message.modelId, target_file: message.targetFile || "auth_service.py" }, (err, data) => {
                        webviewView.webview.postMessage({
                            command: 'sendVibeResponse',
                            success: !err,
                            data: data,
                            error: err ? err.message : null
                        });
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

    _callBackend(path, payload, callback) {
        const postData = JSON.stringify(payload);
        const options = {
            hostname: '127.0.0.1',
            port: 5000,
            path: path,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

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

    _getHtmlForWebview(webview) {
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.js'));
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.css'));
        const htmlUri = vscode.Uri.joinPath(this._extensionUri, 'media', 'chat.html');

        // 파일 읽기
        const fs = require('fs');
        let htmlContent = '';
        try {
            htmlContent = fs.readFileSync(htmlUri.fsPath, 'utf8');
        } catch (e) {
            htmlContent = '<html><body><h3>Error loading Chat UI</h3></body></html>';
        }

        // 경로 치환
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
