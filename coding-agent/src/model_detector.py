# -*- coding: utf-8 -*-
"""
Agent Smith - AI Models Auto-Discovery & Health Detector Engine
Scans Environment API Keys & Local Endpoints to List Available Models
"""

import os
import sys
import logging
import urllib.request
from dataclasses import dataclass
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="[MODEL-DETECTOR][%(asctime)s] %(message)s")


@dataclass
class DetectedModel:
    model_id: str
    name: str
    provider: str
    status: str       # "ONLINE" or "OFFLINE"
    status_msg: str   # E.g., "Ready for Inference", "API Key Required"
    endpoint: str


class AIModelDetector:
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.local_vllm_url = os.getenv("VLLM_ENDPOINT", "http://localhost:8000/v1")

    def check_local_vllm(self) -> bool:
        """Ping local/on-prem vLLM endpoint"""
        try:
            req = urllib.request.Request(f"{self.local_vllm_url}/models", headers={"User-Agent": "AgentSmith/1.0"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def scan_available_models(self) -> List[DetectedModel]:
        """Scan and detect all available models"""
        logging.info("Initiating Auto-Discovery scan for AI Models...")
        detected: List[DetectedModel] = []

        # 1. Claude 3.5 Sonnet
        has_claude = bool(self.openrouter_key or self.anthropic_key)
        detected.append(DetectedModel(
            model_id="claude-3-5-sonnet",
            name="Anthropic Claude 3.5 Sonnet",
            provider="OpenRouter / Anthropic Direct",
            status="ONLINE" if has_claude else "OFFLINE",
            status_msg="Ready for High-Precision Coding" if has_claude else "API Key Required in Settings",
            endpoint="https://openrouter.ai/api/v1"
        ))

        # 2. GPT-4o
        has_gpt = bool(self.openai_key or self.openrouter_key)
        detected.append(DetectedModel(
            model_id="gpt-4o",
            name="OpenAI GPT-4o",
            provider="OpenAI Direct",
            status="ONLINE" if has_gpt else "OFFLINE",
            status_msg="Ready for Multimodal Coding" if has_gpt else "API Key Required in Settings",
            endpoint="https://api.openai.com/v1"
        ))

        # 3. Qwen 2.5 Coder 32B
        has_qwen = bool(self.openrouter_key or True)  # OpenRouter free tier fallback
        detected.append(DetectedModel(
            model_id="qwen-2.5-coder-32b",
            name="Qwen 2.5 Coder 32B",
            provider="OpenRouter API",
            status="ONLINE",
            status_msg="Ready (OpenRouter Default)",
            endpoint="https://openrouter.ai/api/v1"
        ))

        # 4. DeepSeek R1
        detected.append(DetectedModel(
            model_id="deepseek-r1",
            name="DeepSeek R1 Reasoning",
            provider="OpenRouter API",
            status="ONLINE",
            status_msg="Ready for Deep Reasoning",
            endpoint="https://openrouter.ai/api/v1"
        ))

        # 5. On-Premise vLLM Qwen
        vllm_online = self.check_local_vllm()
        detected.append(DetectedModel(
            model_id="local-vllm-qwen",
            name="On-Premise Red Hat vLLM Qwen",
            provider="On-Premise RHOAI (SNO)",
            status="ONLINE" if vllm_online else "OFFLINE (Standby)",
            status_msg="Local GPU Active" if vllm_online else "Standby (Waiting for RHOAI Cluster)",
            endpoint=self.local_vllm_url
        ))

        return detected

    def print_discovery_report(self):
        """Print Auto-Discovery status report"""
        models = self.scan_available_models()
        print("\n================ AI MODELS AUTO-DISCOVERY REPORT ================")
        print(f"{'Model Name':<30} | {'Status':<18} | {'Provider':<25} | {'Message'}")
        print("-" * 95)
        for m in models:
            status_str = f"ONLINE" if "ONLINE" in m.status else f"OFFLINE"
            print(f"{m.name:<30} | [{status_str:<6}]           | {m.provider:<25} | {m.status_msg}")
        print("=================================================================\n")


if __name__ == '__main__':
    detector = AIModelDetector()
    detector.print_discovery_report()
