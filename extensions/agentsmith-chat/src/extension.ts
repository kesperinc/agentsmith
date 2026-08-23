import * as vscode from 'vscode';
import { AgentSmithChatViewProvider } from './chatViewProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('[Agent Smith] Intelligent Studio Extension Activated.');

    const provider = new AgentSmithChatViewProvider(context.extensionUri);

    // 1. Webview View Provider 등록 (사이드바 / 액티비티 바)
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            AgentSmithChatViewProvider.viewType,
            provider,
            { webviewOptions: { retainContextWhenHidden: true } }
        )
    );

    // 2. 명령어 등록 (사이드바 및 중앙 에디터 열기)
    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openChat', () => {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        })
    );

    // 3. 명령어 등록 (에디터 내 중앙 3-Panel 스튜디오 열기)
    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openEditorPanel', () => {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        })
    );

    // 4. 데스크톱 앱 시작 시 Welcome 위치(중앙 에디터 영역)에 Agent Smith Studio 자동 실행
    setTimeout(() => {
        try {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        } catch (e) {
            console.error('[Agent Smith] Failed to auto-open Studio Editor Panel:', e);
        }
    }, 250);
}

export function deactivate() {
    console.log('[Agent Smith] Intelligent Studio Extension Deactivated.');
}
