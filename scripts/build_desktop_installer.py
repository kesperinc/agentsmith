# -*- coding: utf-8 -*-
"""
Agent Smith Enterprise Desktop Single Setup Installer Builder
Compiles dist/agentsmith-desktop-v1.0.0/ into a single standalone Windows Setup Executable:
dist/AgentSmith_Desktop_Setup_v1.0.0.exe using Windows Native C# Compiler (csc.exe).
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
SOURCE_DIST = DIST_DIR / "agentsmith-desktop-v1.0.0"
SETUP_EXE_OUT = DIST_DIR / "AgentSmith_Desktop_Setup_v1.0.0.exe"
BUILD_TEMP = DIST_DIR / "installer_build_temp"

print("==================================================")
print("[Agent Smith] Building Native Windows Setup Executable...")
print(f"Source Directory: {SOURCE_DIST}")
print(f"Output Executable: {SETUP_EXE_OUT}")
print("==================================================")

if not SOURCE_DIST.exists():
    print(f"[ERROR] Source package {SOURCE_DIST} does not exist.")
    sys.exit(1)

# 1. Prepare Staging
if BUILD_TEMP.exists():
    shutil.rmtree(BUILD_TEMP, ignore_errors=True)
BUILD_TEMP.mkdir(parents=True, exist_ok=True)

PAYLOAD_ZIP = BUILD_TEMP / "payload.zip"
INSTALLER_CS = BUILD_TEMP / "Installer.cs"

# 2. Compress Payload into payload.zip
print("[1/3] Compressing application payload into binary zip stream...")
with zipfile.ZipFile(PAYLOAD_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(SOURCE_DIST):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(SOURCE_DIST)
            zipf.write(file_path, arcname)

print(f"[ok] Payload zip created ({os.path.getsize(PAYLOAD_ZIP) / (1024*1024):.2f} MB)")

# 3. Generate C# Installer Source Code: Installer.cs
CS_SOURCE = r'''using System;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Diagnostics;
using System.Windows.Forms;

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

                DialogResult result = MessageBox.Show(
                    "Agent Smith Enterprise Desktop IDE를 설치하시겠습니까?\n\n설치 경로: " + targetDir,
                    "Agent Smith Desktop IDE Setup",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Question
                );

                if (result != DialogResult.Yes) return;

                if (!Directory.Exists(targetDir))
                {
                    Directory.CreateDirectory(targetDir);
                }

                // Extract embedded resource payload.zip
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

                // Extract payload files (.NET Framework 4.5 ZipFile API)
                ZipFile.ExtractToDirectory(tempZipPath, targetDir);

                if (File.Exists(tempZipPath))
                {
                    File.Delete(tempZipPath);
                }

                // Create Shortcuts using PowerShell Script
                string psScript = "$TargetDir = '" + targetDir.Replace(@"\", @"\\") + "'; " +
                    "$ExePath = Join-Path $TargetDir 'run_agentsmith_desktop.bat'; " +
                    "$IconPath = Join-Path $TargetDir 'app\\resources\\win32\\code.ico'; " +
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
                    string runnerBat = Path.Combine(targetDir, "run_agentsmith_desktop.bat");
                    ProcessStartInfo runInfo = new ProcessStartInfo("cmd.exe", "/c \"" + runnerBat + "\"");
                    runInfo.WorkingDirectory = targetDir;
                    runInfo.CreateNoWindow = true;
                    runInfo.UseShellExecute = false;
                    Process.Start(runInfo);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("설치 중 오류가 발생했습니다:\n" + ex.Message, "설치 에러", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
'''

with open(INSTALLER_CS, "w", encoding="utf-8") as f:
    f.write(CS_SOURCE)

print("[2/3] Created C# Installer source code.")

# 4. Compile with C# Compiler (csc.exe)
CSC_PATH = r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
print(f"[3/3] Compiling Native Setup Executable with {CSC_PATH}...")

cmd = [
    CSC_PATH,
    "/target:winexe",
    f"/res:{PAYLOAD_ZIP},payload.zip",
    f"/out:{SETUP_EXE_OUT}",
    "/r:System.Windows.Forms.dll",
    "/r:System.IO.Compression.dll",
    "/r:System.IO.Compression.FileSystem.dll",
    str(INSTALLER_CS)
]

proc = subprocess.run(cmd, capture_output=True, text=True)

if proc.returncode == 0:
    print("==================================================")
    print(f"[SUCCESS] Native Setup Executable Built Successfully!")
    print(f"Setup File: {SETUP_EXE_OUT}")
    print(f"File Size: {os.path.getsize(SETUP_EXE_OUT) / (1024*1024):.2f} MB")
    print("==================================================")
    
    # Cleanup Temp
    shutil.rmtree(BUILD_TEMP, ignore_errors=True)
else:
    print("[ERROR] Compilation failed:")
    print(proc.stdout)
    print(proc.stderr)
    sys.exit(1)
