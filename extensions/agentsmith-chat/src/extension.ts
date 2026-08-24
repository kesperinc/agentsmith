import * as vscode from 'vscode';
import { AgentSmithChatViewProvider } from './chatViewProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('[Agent Smith] Intelligent Studio Extension Activated.');

    // 1. 명령어 등록 (중앙 3-Panel 스튜디오 열기)
    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openChat', () => {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('agentsmith.openEditorPanel', () => {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
        })
    );

    // 2. 데스크톱 앱 시작 시:
    //   - Welcome 위치(중앙 에디터 영역 ViewColumn 1)에 Agent Smith Studio 자동 실행
    //   - 좌측 사이드바는 파일 탐색기(Explorer)로 전환하여 3창 레이아웃 구성
    setTimeout(() => {
        try {
            AgentSmithChatViewProvider.createOrShowEditorPanel(context.extensionUri);
            vscode.commands.executeCommand('workbench.view.explorer');
        } catch (e) {
            console.error('[Agent Smith] Failed to auto-open Studio Editor Panel:', e);
        }
    }, 250);
}

export function deactivate() {
    console.log('[Agent Smith] Intelligent Studio Extension Deactivated.');
}
