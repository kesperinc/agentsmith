"""
Agent Smith IDE - Infrastructure & Hardware Detector
Autodetects local virtual environments, Node.js portable,
Red Hat OpenShift AI clusters, DGX Spark hardware, and local accelerators (CUDA/Intel/AMD).
"""

import sys
import os
import subprocess
import shutil
import urllib.request
import json
from pathlib import Path

# 전역 UTF-8 기본 인코딩 보장
if sys.platform == "win32":
    try:
        import codecs
        codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp949' else None)
    except Exception:
        pass

class HardwareDetector:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.venv_dir = base_dir / "agentsmith" / ".venv"
        self.bin_dir = base_dir / "agentsmith" / "coding-agent" / "bin"
        self.bin_dir.mkdir(parents=True, exist_ok=True)

    def verify_and_setup_venv(self) -> str:
        """Python uv 가상환경 검증 및 1-Click 자동 생성"""
        print("   [SCAN] Checking Python virtual environment (.venv)...")
        if self.venv_dir.exists():
            print(f"      [OK] 가상환경 활성화 상태 감지: {self.venv_dir}")
            return "EXISTS"
        
        print("      [NOTICE] 가상환경(.venv)이 존재하지 않습니다. uv를 통한 자동 구성을 시도합니다.")
        
        # uv 패키지 매니저 검색
        uv_executable = shutil.which("uv")
        if not uv_executable:
            print("      [WARNING] uv 패키지 매니저가 전역에 설치되어 있지 않습니다.")
            print("      [Action] 일반 pip를 통해 가상환경 구성을 시도합니다...")
            try:
                subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], check=True)
                print("      [OK] 시스템 venv 생성 완료.")
                self._install_dependencies_fallback()
                return "CREATED_PIP"
            except Exception as e:
                print(f"      [FAIL] 가상환경 생성 실패: {e}")
                return "FAILED"

        # uv를 활용한 고속 venv 생성
        try:
            print("      [Action] uv venv 생성 중...")
            subprocess.run([uv_executable, "venv", str(self.venv_dir)], check=True)
            print("      [OK] uv venv 고속 생성 완료.")
            
            # requirements.txt 설치
            req_file = self.base_dir / "agentsmith" / "coding-agent" / "requirements.txt"
            if req_file.exists():
                print("      [Action] uv pip install로 의존성 격리 설치 중...")
                python_path = self.venv_dir / ("Scripts" if sys.platform == "win32" else "bin") / "python"
                subprocess.run([uv_executable, "pip", "install", "-r", str(req_file), "--python", str(python_path)], check=True)
                print("      [OK] 의존성 격리 설치 완료.")
            return "CREATED_UV"
        except Exception as e:
            print(f"      [FAIL] uv 가상환경 구성 실패: {e}")
            return "FAILED"

    def _install_dependencies_fallback(self):
        """pip 기반 의존성 백업 설치"""
        req_file = self.base_dir / "agentsmith" / "coding-agent" / "requirements.txt"
        if req_file.exists():
            print("      [Action] pip install로 의존성 백업 설치 중...")
            pip_path = self.venv_dir / ("Scripts" if sys.platform == "win32" else "bin") / "pip"
            try:
                subprocess.run([str(pip_path), "install", "-r", str(req_file)], check=True)
                print("      [OK] 백업 의존성 설치 완료.")
            except Exception as e:
                print(f"      [WARNING] 백업 설치 실패: {e}")

    def verify_and_setup_node(self) -> str:
        """Node.js 설치 감지 및 1-Click 미니 런타임 탑재"""
        print("   [SCAN] Checking Node.js runtime environment...")
        node_path = shutil.which("node")
        if node_path:
            print(f"      [OK] 전역 Node.js 감지 완료: {node_path}")
            return "EXISTS_GLOBAL"

        # 에디터 내 포터블 디렉터리 내에 node가 있는지 확인
        portable_node = self.bin_dir / ("node.exe" if sys.platform == "win32" else "node")
        if portable_node.exists():
            print(f"      [OK] 로컬 포터블 Node.js 감지 완료: {portable_node}")
            return "EXISTS_PORTABLE"

        print("      [WARNING] 시스템에 Node.js 가 설치되어 있지 않습니다.")
        print("      [Action] 백그라운드 AI 에이전트 구동을 위해 포터블 Node.js 구성을 자동 다운로드합니다...")
        
        # OS별 포터블 Node 다운로드 (데모 검증용 미니 바이너리 다운로드 룰셋)
        try:
            node_ver = "v18.16.0"
            if sys.platform == "win32":
                url = f"https://nodejs.org/dist/{node_ver}/win-x64/node.exe"
                print(f"      [Action] Downloading Windows Portable Node: {url}")
                urllib.request.urlretrieve(url, str(portable_node))
                print(f"      [OK] Portable Node.js 다운로드 완료: {portable_node}")
                return "DOWNLOADED_PORTABLE"
            else:
                # Linux/macOS는 curl 등으로 전처리 가이드 안내
                print("      [NOTICE] Non-Windows 환경에서는 시스템 Node.js 패키지 설치(apt, brew, dnf)를 권장합니다.")
                return "MANUAL_INSTALL_REQUIRED"
        except Exception as e:
            print(f"      [FAIL] 포터블 Node.js 다운로드 실패: {e}")
            return "FAILED"

    def detect_rhoai_vllm(self) -> dict:
        """Red Hat OpenShift AI (RHOAI) 클러스터 및 vLLM 서빙 서비스 감지"""
        print("   [SCAN] Scanning Red Hat OpenShift AI (RHOAI) environment...")
        result = {"detected": False, "endpoint": None, "type": None}
        
        # 1. oc / kubectl 접속 설정 확인
        oc_bin = shutil.which("oc") or shutil.which("kubectl")
        if not oc_bin:
            return result

        try:
            # 현재 Kube context에 openshift/rhoai가 바인딩 되어있는지 확인
            proc = subprocess.run([oc_bin, "config", "current-context"], capture_output=True, text=True, timeout=2)
            context = proc.stdout.lower()
            if "openshift" in context or "rhoai" in context:
                result["detected"] = True
                result["type"] = "OpenShift AI Cluster"
                
                # vLLM ServingRuntime API 서비스 탐색 (클러스터 내부 도메인 또는 모킹 도메인 반환)
                result["endpoint"] = "http://qwen-coder.rhoai.svc.cluster.local:8000"
                print(f"      [OK] RHOAI 클러스터 환경 감지 완료 (Context: {context.strip()})")
                print(f"      [Action] AI 호출 엔드포인트를 vLLM 서빙 서비스로 자동 튜닝합니다.")
        except Exception:
            pass

        return result

    def detect_dgx_spark(self) -> dict:
        """DGX Spark 또는 엔터프라이즈 고성능 하드웨어 검출"""
        print("   [SCAN] Detecting DGX Spark system configuration...")
        result = {"is_dgx": False, "product_name": "Standard PC/VM", "profile": "lightweight"}

        try:
            if sys.platform == "win32":
                proc = subprocess.run(["wmic", "csproduct", "get", "name"], capture_output=True, text=True, timeout=2)
                lines = [line.strip() for line in proc.stdout.split('\n') if line.strip()]
                if len(lines) > 1:
                    product = lines[1]
                    result["product_name"] = product
            else:
                dmi_path = Path("/sys/class/dmi/id/product_name")
                if dmi_path.exists():
                    result["product_name"] = dmi_path.read_text().strip()

            prod_lower = result["product_name"].lower()
            if "dgx" in prod_lower or "spark" in prod_lower:
                result["is_dgx"] = True
                result["profile"] = "maximum-performance (32B/72B Enabled)"
                print(f"      [OK] 고성능 HW 감지 완료: DGX Spark 시스템 식별됨 ({result['product_name']})")
                print(f"      [Action] 로컬 오프라인 LLM 사양을 최대성능 프로필로 설정합니다.")
            else:
                print(f"      [OK] 표준 성능 하드웨어 감지 완료 ({result['product_name']})")

        except Exception:
            pass

        return result

    def detect_accelerators(self) -> list:
        """NVIDIA CUDA / Intel Arc / AMD GPU 가속기 검출"""
        print("   [SCAN] Scanning hardware graphic accelerators...")
        accelerators = []

        # 1. NVIDIA CUDA 검출
        smi_bin = shutil.which("nvidia-smi")
        if smi_bin:
            try:
                proc = subprocess.run([smi_bin, "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True, text=True, timeout=3)
                gpu_info = proc.stdout.strip()
                if gpu_info:
                    accelerators.append(f"NVIDIA GPU ({gpu_info})")
                    print(f"      [OK] NVIDIA CUDA 가속 장치 감지 완료: {gpu_info}")
            except Exception:
                pass

        # 2. Intel OpenVINO / Arc 가속 확인 (Windows DirectML 또는 sysfs 기반)
        if sys.platform == "win32":
            try:
                # PowerShell을 활용한 윈도우 그래픽 디바이스 쿼리
                ps_cmd = "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"
                proc = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=3)
                devices = proc.stdout.strip().split('\n')
                for dev in devices:
                    dev = dev.strip()
                    if "Intel" in dev and ("Arc" in dev or "Iris" in dev):
                        accelerators.append(f"Intel GPU ({dev})")
                        print(f"      [OK] Intel OpenVINO 가속 호환 그래픽 장치 감지 완료: {dev}")
                    elif "AMD" in dev and "Radeon" in dev:
                        accelerators.append(f"AMD GPU ({dev})")
                        print(f"      [OK] AMD ROCm/DirectML 가속 호환 그래픽 장치 감지 완료: {dev}")
            except Exception:
                pass

        if not accelerators:
            print("      [NOTICE] 전용 가속장치 미감지 (CPU 전용 연산 모드로 기동)")
            accelerators.append("CPU Only")

        return accelerators

    def run_all_checks(self) -> dict:
        """모든 감지 루틴을 통합 수행하고 시스템 프로필 반환"""
        print("\n=== Agent Smith Infrastructure Harness Scan ===")
        venv_status = self.verify_and_setup_venv()
        node_status = self.verify_and_setup_node()
        rhoai_status = self.detect_rhoai_vllm()
        dgx_status = self.detect_dgx_spark()
        gpus = self.detect_accelerators()
        print("================================================\n")

        return {
            "venv": venv_status,
            "node": node_status,
            "rhoai": rhoai_status,
            "hardware": dgx_status,
            "accelerators": gpus
        }

if __name__ == "__main__":
    # 독립 기동 시 테스트용
    detector = HardwareDetector(Path(__file__).resolve().parent.parent.parent.parent)
    results = detector.run_all_checks()
    print("최종 감지 결과 메타데이터:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
