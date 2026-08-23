import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export class AgentSmithChatViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'agentsmith.chatView';
    private _view?: vscode.WebviewView;
    private static currentEditorPanel?: vscode.WebviewPanel;

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        _context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Webview 메시지 수신 핸들러
        webviewView.webview.onDidReceiveMessage(async (data) => {
            await this._handleMessage(data);
        });
    }

    public static createOrShowEditorPanel(extensionUri: vscode.Uri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (AgentSmithChatViewProvider.currentEditorPanel) {
            AgentSmithChatViewProvider.currentEditorPanel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'agentsmithStudioPanel',
            'Agent Smith Studio',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        const provider = new AgentSmithChatViewProvider(extensionUri);
        panel.webview.html = provider._getHtmlForWebview(panel.webview);

        panel.webview.onDidReceiveMessage(async (data) => {
            await provider._handleMessage(data);
        });

        panel.onDidDispose(() => {
            AgentSmithChatViewProvider.currentEditorPanel = undefined;
        });

        AgentSmithChatViewProvider.currentEditorPanel = panel;
    }

    private async _handleMessage(data: any) {
        switch (data.command) {
            case 'openEditorPanel': {
                AgentSmithChatViewProvider.createOrShowEditorPanel(this._extensionUri);
                break;
            }
            case 'openFile': {
                if (data.path) {
                    const workspaceFolders = vscode.workspace.workspaceFolders;
                    let targetUri: vscode.Uri;

                    if (path.isAbsolute(data.path)) {
                        targetUri = vscode.Uri.file(data.path);
                    } else if (workspaceFolders && workspaceFolders.length > 0) {
                        targetUri = vscode.Uri.file(path.join(workspaceFolders[0].uri.fsPath, data.path));
                    } else {
                        targetUri = vscode.Uri.file(data.path);
                    }

                    try {
                        const doc = await vscode.workspace.openTextDocument(targetUri);
                        await vscode.window.showTextDocument(doc, { preview: false });
                    } catch (e) {
                        vscode.window.showWarningMessage(`문서를 열 수 없습니다: ${data.path}`);
                    }
                }
                break;
            }
            case 'acceptDiff': {
                vscode.window.showInformationMessage(`[Agent Smith] ${data.file || '파일'}의 변경사항이 수락되어 작업공간에 반영되었습니다.`);
                break;
            }
            case 'rollbackDiff': {
                vscode.window.showInformationMessage(`[Agent Smith] ${data.file || '파일'}의 변경사항이 원본으로 롤백되었습니다.`);
                break;
            }
            case 'notify': {
                if (data.type === 'error') {
                    vscode.window.showErrorMessage(`[Agent Smith] ${data.message}`);
                } else {
                    vscode.window.showInformationMessage(`[Agent Smith] ${data.message}`);
                }
                break;
            }
        }
    }

    private _getHtmlForWebview(webview: vscode.Webview): string {
        const mediaPath = path.join(this._extensionUri.fsPath, 'media');
        const indexPath = path.join(mediaPath, 'index.html');

        let html = '';
        try {
            html = fs.readFileSync(indexPath, 'utf-8');
        } catch (e) {
            html = `<!DOCTYPE html><html><body><h3>Agent Smith Studio Loading...</h3></body></html>`;
        }

        const styleUri = webview.asWebviewUri(vscode.Uri.file(path.join(mediaPath, 'style.css')));
        const scriptUri = webview.asWebviewUri(vscode.Uri.file(path.join(mediaPath, 'app.js')));

        html = html.replace('href="style.css"', `href="${styleUri}"`);
        html = html.replace('src="app.js"', `src="${scriptUri}"`);

        return html;
    }
}
