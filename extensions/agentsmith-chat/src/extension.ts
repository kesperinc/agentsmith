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

    // 2. 명령어 등록 (사이드바 열기)
    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openChat', () => {
            vscode.commands.executeCommand('workbench.view.extension.agentsmith-chat-container');
        })
    );

    // 3. 명령어 등록 (에디터 내 중앙 3-Panel 스튜디오 열기)
    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openEditorPanel', () => {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        })
    );
}

export function deactivate() {
    console.log('[Agent Smith] Intelligent Studio Extension Deactivated.');
}
