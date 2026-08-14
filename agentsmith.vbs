Set WshShell = CreateObject("WScript.Shell")
' 2026-08-14_run_desktop.bat 배치 파일을 창 없이(0 = SW_HIDE, false = 비동기) 실행
WshShell.Run "cmd.exe /c 2026-08-14_run_desktop.bat", 0, false
