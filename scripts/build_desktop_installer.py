# -*- coding: utf-8 -*-
"""
Agent Smith Enterprise Desktop Single Setup Executable Compiler
Compiles a standalone C# Windows installer with embedded zip payload,
progress bar GUI, automatic uninstallation of older versions, and shortcut creation.
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

# Force UTF-8 Output
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
SOURCE_PAYLOAD_DIR = DIST_DIR / "agentsmith-desktop-v1.0.0"
PAYLOAD_ZIP = DIST_DIR / "temp_payload.zip"
CS_INSTALLER_SRC = DIST_DIR / "Installer.cs"
SETUP_EXE_PATH = DIST_DIR / "AgentSmith_Desktop_Setup_v1.0.0.exe"
BRAND_ICON = ROOT_DIR / "docs" / "images" / "code.ico"

print("=" * 50)
print("[Agent Smith] Building Native Windows Setup Executable with Progress Bar...")
print(f"Source Directory: {SOURCE_PAYLOAD_DIR}")
print(f"Output Executable: {SETUP_EXE_PATH}")
print("=" * 50)

# 1. Verify Payload Directory
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

# 3. Generate C# Installer Source Code with Windows Forms Progress Bar: Installer.cs
CS_SOURCE = r'''using System;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Diagnostics;
using System.Windows.Forms;
using System.Drawing;
using System.Threading;

namespace AgentSmithInstaller
{
    public class InstallProgressForm : Form
    {
        public ProgressBar ProgressBar;
        public Label StatusLabel;
        public Label FileLabel;
        public Label TitleLabel;

        public InstallProgressForm()
        {
            this.Text = "Agent Smith Enterprise Desktop IDE 설치";
            this.Size = new Size(540, 240);
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.FromArgb(245, 246, 250);
            this.Font = new Font("Malgun Gothic", 9F, FontStyle.Regular);

            TitleLabel = new Label();
            TitleLabel.Text = "Agent Smith Desktop IDE를 설치하는 중입니다...";
            TitleLabel.Font = new Font("Malgun Gothic", 11F, FontStyle.Bold);
            TitleLabel.ForeColor = Color.FromArgb(20, 20, 30);
            TitleLabel.Location = new Point(25, 20);
            TitleLabel.AutoSize = true;
            this.Controls.Add(TitleLabel);

            StatusLabel = new Label();
            StatusLabel.Text = "설치 준비 중...";
            StatusLabel.Font = new Font("Malgun Gothic", 9.5F, FontStyle.Regular);
            StatusLabel.ForeColor = Color.FromArgb(60, 60, 80);
            StatusLabel.Location = new Point(25, 60);
            StatusLabel.AutoSize = true;
            this.Controls.Add(StatusLabel);

            ProgressBar = new ProgressBar();
            ProgressBar.Location = new Point(25, 90);
            ProgressBar.Size = new Size(475, 26);
            ProgressBar.Minimum = 0;
            ProgressBar.Maximum = 100;
            ProgressBar.Value = 0;
            ProgressBar.Style = ProgressBarStyle.Continuous;
            this.Controls.Add(ProgressBar);

            FileLabel = new Label();
            FileLabel.Text = "";
            FileLabel.Font = new Font("Malgun Gothic", 8F, FontStyle.Regular);
            FileLabel.ForeColor = Color.FromArgb(120, 120, 140);
            FileLabel.Location = new Point(25, 125);
            FileLabel.Size = new Size(475, 40);
            FileLabel.AutoEllipsis = true;
            this.Controls.Add(FileLabel);
        }

        public void UpdateProgress(int percent, string status, string currentFile)
        {
            if (this.InvokeRequired)
            {
                this.Invoke(new Action<int, string, string>(UpdateProgress), percent, status, currentFile);
                return;
            }
            if (percent >= 0 && percent <= 100)
            {
                this.ProgressBar.Value = percent;
            }
            if (!string.IsNullOrEmpty(status))
            {
                this.StatusLabel.Text = status;
            }
            if (currentFile != null)
            {
                this.FileLabel.Text = currentFile;
            }
            this.Refresh();
        }
    }

    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            try
            {
                EnsureLongPathSupport();

                string defaultTarget = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "Programs",
                    "AgentSmith"
                );

                string targetDir = defaultTarget;

                if (defaultTarget.Length > 55)
                {
                    DialogResult pathChoice = MessageBox.Show(
                        "현재 Windows 사용자 계정 경로가 길어 Windows MAX_PATH(260자) 제한을 예방하기 위해\n" +
                        "단축 설치 경로(C:\\AgentSmith)에 설치하는 것을 권장합니다.\n\n" +
                        "기본 경로: " + defaultTarget + " (" + defaultTarget.Length + "자)\n" +
                        "권장 단축 경로: C:\\AgentSmith\n\n" +
                        "[예(Yes)] 권장 단축 경로(C:\\AgentSmith)에 설치\n" +
                        "[아니오(No)] 기본 AppData 경로에 설치",
                        "Agent Smith 설치 경로 최적화 안내",
                        MessageBoxButtons.YesNo,
                        MessageBoxIcon.Question
                    );

                    if (pathChoice == DialogResult.Yes)
                    {
                        targetDir = @"C:\AgentSmith";
                    }
                }

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

                // 모던 설치 진행상황 다이얼로그 생성 및 표시
                InstallProgressForm progressForm = new InstallProgressForm();
                progressForm.Show();
                progressForm.UpdateProgress(5, "실행 중인 프로세스 정리 중...", "");
                Application.DoEvents();

                // 1단계: 실행 중인 잠금 프로세스 전면 강제 종료
                KillLockedProcesses(targetDir);

                // 2단계: 클린 설치 시 기존 디렉터리 안전 삭제
                if (cleanInstall)
                {
                    progressForm.UpdateProgress(10, "기존 설치 디렉터리 정리 중...", targetDir);
                    Application.DoEvents();

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
                        if (retryDel != DialogResult.Yes)
                        {
                            progressForm.Close();
                            return;
                        }
                    }
                }

                if (!Directory.Exists(targetDir))
                {
                    Directory.CreateDirectory(targetDir);
                }

                // 3단계: 임베디드 리소스 payload.zip 추출
                progressForm.UpdateProgress(15, "설치 패키지 데이터 로드 중...", "payload.zip 추출 중...");
                Application.DoEvents();

                string tempZipPath = Path.Combine(Path.GetTempPath(), "agentsmith_install_payload_" + Guid.NewGuid().ToString("N") + ".zip");
                
                Assembly assembly = Assembly.GetExecutingAssembly();
                using (Stream stream = assembly.GetManifestResourceStream("payload.zip"))
                {
                    if (stream == null)
                    {
                        progressForm.Close();
                        MessageBox.Show("설치 리소스를 로드할 수 없습니다.", "설치 오류", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                    using (FileStream fs = new FileStream(tempZipPath, FileMode.Create, FileAccess.Write))
                    {
                        stream.CopyTo(fs);
                    }
                }

                // 4단계: Safe Multi-Retry / Rename 오버라이트 추출 및 실시간 프로그레스 바 업데이트
                using (ZipArchive archive = ZipFile.OpenRead(tempZipPath))
                {
                    int totalEntries = archive.Entries.Count;
                    int currentEntry = 0;

                    foreach (ZipArchiveEntry entry in archive.Entries)
                    {
                        currentEntry++;
                        int percent = 20 + (int)((double)currentEntry / totalEntries * 70); // 20% ~ 90%
                        
                        string destinationPath = Path.GetFullPath(Path.Combine(targetDir, entry.FullName));
                        if (!destinationPath.StartsWith(Path.GetFullPath(targetDir), StringComparison.OrdinalIgnoreCase))
                        {
                            continue;
                        }

                        if (currentEntry % 15 == 0 || currentEntry == totalEntries)
                        {
                            string displayFile = entry.FullName;
                            if (displayFile.Length > 55) displayFile = "..." + displayFile.Substring(displayFile.Length - 52);
                            progressForm.UpdateProgress(percent, string.Format("파일 설치 중: {0}% ({1} / {2})", percent, currentEntry, totalEntries), displayFile);
                            Application.DoEvents();
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

                // 5단계: 바탕화면 및 시작메뉴 바로가기 생성
                progressForm.UpdateProgress(92, "바탕화면 및 시작 메뉴 바로가기 구성 중...", "Agent Smith Desktop IDE.lnk");
                Application.DoEvents();

                string psScript = "$TargetDir = '" + targetDir.Replace(@"\", @"\\") + "'; " +
                    "$ExePath = Join-Path $TargetDir 'run_agentsmith_desktop.bat'; " +
                    "$IconPath = Join-Path $TargetDir 'resources\\code.ico'; " +
                    "if (!(Test-Path $IconPath)) { $IconPath = Join-Path $TargetDir 'app\\resources\\win32\\code.ico'; } " +
                    "if (!(Test-Path $IconPath)) { $IconPath = Join-Path $TargetDir 'app\\AgentSmith.exe'; } " +
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

                // 6단계: 환경변수 가드레일 주입
                progressForm.UpdateProgress(98, "환경 변수 설정 및 보안 가드레일 검증 중...", "USERPROFILE / APPDATA / UTF-8");
                Application.DoEvents();

                try
                {
                    string curUp = Environment.GetEnvironmentVariable("USERPROFILE", EnvironmentVariableTarget.User);
                    if (string.IsNullOrEmpty(curUp))
                    {
                        string safeUp = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                        if (!string.IsNullOrEmpty(safeUp))
                        {
                            Environment.SetEnvironmentVariable("USERPROFILE", safeUp, EnvironmentVariableTarget.User);
                        }
                    }
                    Environment.SetEnvironmentVariable("PYTHONUTF8", "1", EnvironmentVariableTarget.User);
                    Environment.SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", EnvironmentVariableTarget.User);
                }
                catch { }

                progressForm.UpdateProgress(100, "설치가 성공적으로 완료되었습니다!", "완료");
                Application.DoEvents();
                Thread.Sleep(500);
                progressForm.Close();

                // 7단계: 완료 안내 및 자동 실행 질의
                DialogResult launchChoice = MessageBox.Show(
                    "Agent Smith Enterprise Desktop IDE 설치가 성공적으로 완료되었습니다!\n\n" +
                    "설치 위치: " + targetDir + "\n" +
                    "바로가기: 바탕화면 및 시작 메뉴에 등록됨\n\n" +
                    "지금 바로 Agent Smith Desktop IDE를 실행하시겠습니까?",
                    "설치 완료 - Agent Smith",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Information
                );

                if (launchChoice == DialogResult.Yes)
                {
                    string batPath = Path.Combine(targetDir, "run_agentsmith_desktop.bat");
                    if (File.Exists(batPath))
                    {
                        ProcessStartInfo runPsi = new ProcessStartInfo("cmd.exe", "/c \"" + batPath + "\"");
                        runPsi.WorkingDirectory = targetDir;
                        runPsi.UseShellExecute = false;
                        
                        string userProf = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                        if (!string.IsNullOrEmpty(userProf))
                        {
                            runPsi.EnvironmentVariables["USERPROFILE"] = userProf;
                            runPsi.EnvironmentVariables["APPDATA"] = Path.Combine(userProf, "AppData", "Roaming");
                            runPsi.EnvironmentVariables["LOCALAPPDATA"] = Path.Combine(userProf, "AppData", "Local");
                        }
                        runPsi.EnvironmentVariables["PYTHONUTF8"] = "1";
                        runPsi.EnvironmentVariables["PYTHONIOENCODING"] = "utf-8";
                        
                        Process.Start(runPsi);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("설치 중 치명적인 오류가 발생했습니다:\n\n" + ex.Message, "설치 실패", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private static void EnsureLongPathSupport()
        {
            try
            {
                using (var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SYSTEM\CurrentControlSet\Control\FileSystem", true))
                {
                    if (key != null)
                    {
                        object val = key.GetValue("LongPathsEnabled");
                        if (val == null || Convert.ToInt32(val) != 1)
                        {
                            key.SetValue("LongPathsEnabled", 1, Microsoft.Win32.RegistryValueKind.DWord);
                        }
                    }
                }
            }
            catch { }
        }

        private static void KillLockedProcesses(string targetDir)
        {
            string[] procNames = new string[] { 
                "Code - OSS", "agentsmith_app", "agentsmith_editor", "Code", "electron", 
                "run_agentsmith_desktop", "agentsmith", "AgentSmith" 
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
                    return;
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
                                return;
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

print("[2/3] Created C# Installer source code with Real-Time Progress Bar GUI.")
with open(CS_INSTALLER_SRC, 'w', encoding='utf-8') as f:
    f.write(CS_SOURCE)

# 4. Locate C# Compiler (csc.exe)
CSC_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\Roslyn\csc.exe",
    r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
    r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe",
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
print("[SUCCESS] Native Setup Executable Built Successfully with Progress Bar!")
print(f"Setup File: {SETUP_EXE_PATH}")
print(f"File Size: {setup_size_mb:.2f} MB")
print("=" * 50)
