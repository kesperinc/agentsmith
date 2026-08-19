"""
Native Windows Setup Installer Builder for Agent Smith IDE
Generates a standalone single-executable setup file (AgentSmith_Desktop_Setup_v1.0.0.exe)
incorporating payload compression, C# compilation, brand logo icon, process auto-killer,
and safe multi-retry / unlock extraction routines.
"""

import os
import sys
import shutil
import zipfile
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
SOURCE_PAYLOAD_DIR = os.path.join(DIST_DIR, "agentsmith-desktop-v1.0.0")
SETUP_EXE_PATH = os.path.join(DIST_DIR, "AgentSmith_Desktop_Setup_v1.0.0.exe")
PAYLOAD_ZIP = os.path.join(DIST_DIR, "payload.zip")
CS_INSTALLER_SRC = os.path.join(DIST_DIR, "Installer.cs")
BRAND_ICON = os.path.join(ROOT_DIR, "docs", "images", "code.ico")

print("=" * 50)
print("[Agent Smith] Building Native Windows Setup Executable...")
print(f"Source Directory: {SOURCE_PAYLOAD_DIR}")
print(f"Output Executable: {SETUP_EXE_PATH}")
print("=" * 50)

# 1. Verify Source Payload Directory
if not os.path.exists(SOURCE_PAYLOAD_DIR):
    print(f"[!] Source payload directory not found: {SOURCE_PAYLOAD_DIR}")
    print("[*] Running scripts/package_desktop_dist.py first...")
    res = subprocess.run([sys.executable, os.path.join(ROOT_DIR, "scripts", "package_desktop_dist.py")])
    if res.returncode != 0:
        print("[ERROR] Failed to prepare payload.")
        sys.exit(1)

# 2. Compress payload directory into payload.zip
print("[1/3] Compressing application payload into binary zip stream...")
if os.path.exists(PAYLOAD_ZIP):
    try:
        os.remove(PAYLOAD_ZIP)
    except Exception:
        pass

with zipfile.ZipFile(PAYLOAD_ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    for root, dirs, files in os.walk(SOURCE_PAYLOAD_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, SOURCE_PAYLOAD_DIR)
            zipf.write(full_path, rel_path)

print(f"[ok] Payload zip created ({os.path.getsize(PAYLOAD_ZIP) / (1024*1024):.2f} MB)")

# 3. Generate C# Installer Source Code: Installer.cs
CS_SOURCE = r'''using System;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Diagnostics;
using System.Windows.Forms;
using System.Threading;

namespace AgentSmithInstaller
{
    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            try
            {
                string targetDir = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "Programs",
                    "AgentSmith"
                );

                bool isAlreadyInstalled = Directory.Exists(targetDir) && (
                    File.Exists(Path.Combine(targetDir, "run_agentsmith_desktop.bat")) ||
                    Directory.Exists(Path.Combine(targetDir, "app"))
                );

                bool cleanInstall = false;

                if (isAlreadyInstalled)
                {
                    DialogResult existChoice = MessageBox.Show(
                        "Agent Smith Enterprise Desktop IDE가 이미 설치되어 있습니다.\n\n" +
                        "설치 경로: " + targetDir + "\n\n" +
                        "기존 설치 폴더를 완전히 정리하고 '새로 설치'를 진행하시겠습니까?\n\n" +
                        "[예(Yes)] 기존 파일 완전 삭제 후 새로 설치 (권장)\n" +
                        "[아니오(No)] 기존 파일 덮어쓰기(업데이트) 설치\n" +
                        "[취소(Cancel)] 설치 종료",
                        "Agent Smith 재설치 / 업데이트 감지",
                        MessageBoxButtons.YesNoCancel,
                        MessageBoxIcon.Question
                    );

                    if (existChoice == DialogResult.Cancel)
                    {
                        return;
                    }
                    else if (existChoice == DialogResult.Yes)
                    {
                        cleanInstall = true;
                    }
                    else
                    {
                        cleanInstall = false;
                    }
                }
                else
                {
                    DialogResult result = MessageBox.Show(
                        "Agent Smith Enterprise Desktop IDE를 설치하시겠습니까?\n\n설치 경로: " + targetDir,
                        "Agent Smith Desktop IDE Setup",
                        MessageBoxButtons.YesNo,
                        MessageBoxIcon.Question
                    );

                    if (result != DialogResult.Yes) return;
                }

                // 1단계: 실행 중인 잠금 프로세스 전면 강제 종료
                KillLockedProcesses(targetDir);

                // 2단계: 클린 설치 시 기존 디렉터리 안전 삭제
                if (cleanInstall)
                {
                    bool deleteSuccess = false;
                    for (int attempt = 0; attempt < 3; attempt++)
                    {
                        try
                        {
                            if (Directory.Exists(targetDir))
                            {
                                Directory.Delete(targetDir, true);
                            }
                            deleteSuccess = true;
                            break;
                        }
                        catch
                        {
                            KillLockedProcesses(targetDir);
                            Thread.Sleep(800);
                        }
                    }

                    if (!deleteSuccess && Directory.Exists(targetDir))
                    {
                        DialogResult retryDel = MessageBox.Show(
                            "기존 설치 폴더의 일부 파일이 시스템에서 잠겨 있습니다.\n\n계속해서 안전 덮어쓰기 방식으로 설치를 진행하시겠습니까?",
                            "폴더 정리 알림",
                            MessageBoxButtons.YesNo,
                            MessageBoxIcon.Warning
                        );
                        if (retryDel != DialogResult.Yes) return;
                    }
                }

                if (!Directory.Exists(targetDir))
                {
                    Directory.CreateDirectory(targetDir);
                }

                // 3단계: 임베디드 리소스 payload.zip 추출
                string tempZipPath = Path.Combine(Path.GetTempPath(), "agentsmith_install_payload_" + Guid.NewGuid().ToString("N") + ".zip");
                
                Assembly assembly = Assembly.GetExecutingAssembly();
                using (Stream stream = assembly.GetManifestResourceStream("payload.zip"))
                {
                    if (stream == null)
                    {
                        MessageBox.Show("설치 리소스를 로드할 수 없습니다.", "설치 오류", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                    using (FileStream fs = new FileStream(tempZipPath, FileMode.Create, FileAccess.Write))
                    {
                        stream.CopyTo(fs);
                    }
                }

                // 4단계: Safe Multi-Retry / Rename 오버라이트 추출
                using (ZipArchive archive = ZipFile.OpenRead(tempZipPath))
                {
                    foreach (ZipArchiveEntry entry in archive.Entries)
                    {
                        string destinationPath = Path.GetFullPath(Path.Combine(targetDir, entry.FullName));
                        if (!destinationPath.StartsWith(Path.GetFullPath(targetDir), StringComparison.OrdinalIgnoreCase))
                        {
                            continue;
                        }

                        if (string.IsNullOrEmpty(entry.Name))
                        {
                            Directory.CreateDirectory(destinationPath);
                        }
                        else
                        {
                            SafeExtractEntry(entry, destinationPath, targetDir);
                        }
                    }
                }

                if (File.Exists(tempZipPath))
                {
                    try { File.Delete(tempZipPath); } catch { }
                }

                // 5단계: 바탕화면 및 시작메뉴 바로가기 생성 (PowerShell 스크립트)
                string psScript = "$TargetDir = '" + targetDir.Replace(@"\", @"\\") + "'; " +
                    "$ExePath = Join-Path $TargetDir 'run_agentsmith_desktop.bat'; " +
                    "$IconPath = Join-Path $TargetDir 'resources\\code.ico'; " +
                    "if (!(Test-Path $IconPath)) { $IconPath = Join-Path $TargetDir 'app\\resources\\win32\\code.ico'; } " +
                    "if (!(Test-Path $IconPath)) { $IconPath = Join-Path $TargetDir 'app\\Code - OSS.exe'; } " +
                    "$Wsh = New-Object -ComObject WScript.Shell; " +
                    "$Desktop = [System.Environment]::GetFolderPath('Desktop'); " +
                    "$D = $Wsh.CreateShortcut((Join-Path $Desktop 'Agent Smith Desktop IDE.lnk')); " +
                    "$D.TargetPath = 'cmd.exe'; " +
                    "$D.Arguments = '/c \"\"' + $ExePath + '\"\"'; " +
                    "$D.WorkingDirectory = $TargetDir; " +
                    "$D.IconLocation = $IconPath + ',0'; " +
                    "$D.Description = 'Agent Smith Enterprise Desktop IDE'; " +
                    "$D.Save(); " +
                    "$StartFolder = Join-Path ([System.Environment]::GetFolderPath('Programs')) 'Agent Smith'; " +
                    "if (!(Test-Path $StartFolder)) { New-Item -ItemType Directory -Path $StartFolder -Force | Out-Null } " +
                    "$S = $Wsh.CreateShortcut((Join-Path $StartFolder 'Agent Smith Desktop IDE.lnk')); " +
                    "$S.TargetPath = 'cmd.exe'; " +
                    "$S.Arguments = '/c \"\"' + $ExePath + '\"\"'; " +
                    "$S.WorkingDirectory = $TargetDir; " +
                    "$S.IconLocation = $IconPath + ',0'; " +
                    "$S.Description = 'Agent Smith Enterprise Desktop IDE'; " +
                    "$S.Save();";

                ProcessStartInfo psi = new ProcessStartInfo("powershell", "-NoProfile -ExecutionPolicy Bypass -Command \"" + psScript + "\"");
                psi.CreateNoWindow = true;
                psi.UseShellExecute = false;
                Process.Start(psi).WaitForExit();

                DialogResult launchResult = MessageBox.Show(
                    "Agent Smith Enterprise Desktop IDE 설치가 성공적으로 완료되었습니다!\n\n바탕화면 및 시작 메뉴에 바로가기가 생성되었습니다.\n지금 Agent Smith를 실행하시겠습니까?",
                    "설치 완료",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Information
                );

                if (launchResult == DialogResult.Yes)
                {
                    string launcherPath = Path.Combine(targetDir, "run_agentsmith_desktop.bat");
                    if (File.Exists(launcherPath))
                    {
                        ProcessStartInfo runPsi = new ProcessStartInfo("cmd.exe", "/c \"" + launcherPath + "\"");
                        runPsi.WorkingDirectory = targetDir;
                        runPsi.UseShellExecute = true;
                        Process.Start(runPsi);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("설치 중 오류가 발생했습니다:\n\n" + ex.Message, "설치 오류", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private static void KillLockedProcesses(string targetDir)
        {
            // 1. targetDir 하위에서 실행 중인 모든 프로세스 탐색 및 강제 종료
            try
            {
                string normalizedTarget = Path.GetFullPath(targetDir).TrimEnd('\\', '/') + "\\";
                foreach (Process p in Process.GetProcesses())
                {
                    try
                    {
                        string exePath = "";
                        try { exePath = p.MainModule.FileName; } catch { }
                        if (!string.IsNullOrEmpty(exePath) && exePath.StartsWith(normalizedTarget, StringComparison.OrdinalIgnoreCase))
                        {
                            p.Kill();
                            p.WaitForExit(1500);
                        }
                    }
                    catch { }
                }
            }
            catch { }

            // 2. 프로세스 이름 기반 종료 (Code - OSS, agentsmith_app, agentsmith_editor, electron 등)
            string[] procNames = new string[] { 
                "Code - OSS", "agentsmith_app", "agentsmith_editor", "Code", "electron", 
                "run_agentsmith_desktop", "agentsmith" 
            };
            foreach (var name in procNames)
            {
                try
                {
                    foreach (var p in Process.GetProcessesByName(name))
                    {
                        try { p.Kill(); p.WaitForExit(1500); } catch { }
                    }
                }
                catch { }
            }
        }

        private static void SafeExtractEntry(ZipArchiveEntry entry, string destinationPath, string targetDir)
        {
            string dir = Path.GetDirectoryName(destinationPath);
            if (!Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }

            int maxRetries = 5;
            for (int retry = 0; retry < maxRetries; retry++)
            {
                try
                {
                    if (File.Exists(destinationPath))
                    {
                        try { File.SetAttributes(destinationPath, FileAttributes.Normal); } catch { }
                    }

                    entry.ExtractToFile(destinationPath, true);
                    return; // 성공
                }
                catch (Exception ex)
                {
                    KillLockedProcesses(targetDir);

                    if (retry == maxRetries - 1)
                    {
                        try
                        {
                            string oldPath = destinationPath + ".old_" + Guid.NewGuid().ToString("N").Substring(0, 6);
                            if (File.Exists(destinationPath))
                            {
                                File.Move(destinationPath, oldPath);
                            }
                            entry.ExtractToFile(destinationPath, true);
                            return;
                        }
                        catch
                        {
                            DialogResult res = MessageBox.Show(
                                "다음 파일이 다른 프로그램에 의해 사용 중이거나 잠겨 있어 덮어쓸 수 없습니다:\n\n" +
                                Path.GetFileName(destinationPath) + "\n\n" +
                                "Agent Smith IDE나 관련 프로그램이 켜져 있다면 종료 후 [다시 시도]를 눌러주세요.\n\n" +
                                "[다시 시도 (Retry)]: 덮어쓰기 재시도\n" +
                                "[무시 (Ignore)]: 해당 파일을 건너뛰고 계속 설치\n" +
                                "[취소 (Abort)]: 설치 중단",
                                "파일 잠금 감지",
                                MessageBoxButtons.AbortRetryIgnore,
                                MessageBoxIcon.Warning
                            );

                            if (res == DialogResult.Retry)
                            {
                                retry = 0;
                                continue;
                            }
                            else if (res == DialogResult.Ignore)
                            {
                                return; // 무시하고 다음 파일로 진행
                            }
                            else
                            {
                                throw new Exception("사용자에 의해 설치가 중단되었습니다: " + ex.Message);
                            }
                        }
                    }
                    Thread.Sleep(500);
                }
            }
        }
    }
}
'''

print("[2/3] Created C# Installer source code.")
with open(CS_INSTALLER_SRC, 'w', encoding='utf-8') as f:
    f.write(CS_SOURCE)

# 4. Locate C# Compiler (csc.exe)
CSC_CANDIDATES = [
    r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
    r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe",
    r"C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\Roslyn\csc.exe",
]

csc_path = None
for cand in CSC_CANDIDATES:
    if os.path.exists(cand):
        csc_path = cand
        break

if not csc_path:
    print("[ERROR] C# Compiler (csc.exe) not found on this system.")
    sys.exit(1)

# 5. Compile C# Installer Executable
icon_flag = f"/win32icon:\"{BRAND_ICON}\"" if os.path.exists(BRAND_ICON) else ""
print(f"[3/3] Compiling Native Setup Executable with {csc_path} (Icon: {BRAND_ICON})...")

compile_cmd = f'"{csc_path}" /target:winexe /out:"{SETUP_EXE_PATH}" /resource:"{PAYLOAD_ZIP}",payload.zip /reference:System.IO.Compression.dll /reference:System.IO.Compression.FileSystem.dll /reference:System.Windows.Forms.dll /reference:System.Drawing.dll {icon_flag} "{CS_INSTALLER_SRC}"'

proc = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)

if proc.returncode != 0:
    print("[ERROR] Compilation failed:")
    print(proc.stdout)
    print(proc.stderr)
    sys.exit(1)

# Cleanup intermediate files
try:
    if os.path.exists(PAYLOAD_ZIP):
        os.remove(PAYLOAD_ZIP)
    if os.path.exists(CS_INSTALLER_SRC):
        os.remove(CS_INSTALLER_SRC)
except Exception:
    pass

setup_size_mb = os.path.getsize(SETUP_EXE_PATH) / (1024 * 1024)
print("=" * 50)
print("[SUCCESS] Native Setup Executable Built Successfully!")
print(f"Setup File: {SETUP_EXE_PATH}")
print(f"File Size: {setup_size_mb:.2f} MB")
print("=" * 50)
