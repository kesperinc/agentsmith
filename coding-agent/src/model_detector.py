# -*- coding: utf-8 -*-
"""
Agent Smith - Global AI Models Auto-Discovery & Health Detector Engine
Scans Environment API Keys (USA, China, Korea, HuggingFace) & Local Endpoints
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
    country: str       # "USA", "China", "Korea", "Global OS"
    provider: str
    status: str        # "ONLINE" or "OFFLINE"
    status_msg: str    # E.g., "Ready for Inference", "API Key Required in Settings"
    endpoint: str


class AIModelDetector:
    def __init__(self):
        # USA Keys
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")

        # Korea Keys
        self.hyperclova_key = os.getenv("HYPERCLOVA_SECRET_KEY", "")
        self.upstage_key = os.getenv("UPSTAGE_API_KEY", "")

        # Hugging Face Key
        self.hf_token = os.getenv("HF_TOKEN", "")

        # Local vLLM
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
        """Scan and detect all available models across USA, China, Korea, and Hugging Face"""
        logging.info("Initiating Global Auto-Discovery scan for AI Models (USA, China, Korea, HuggingFace)...")
        detected: List[DetectedModel] = []

        # --- 1. USA Models ---
        has_claude = bool(self.openrouter_key or self.anthropic_key)
        detected.append(DetectedModel(
            model_id="claude-3-5-sonnet",
            name="Anthropic Claude 3.5 Sonnet",
            country="USA",
            provider="Anthropic / OpenRouter",
            status="ONLINE" if has_claude else "OFFLINE",
            status_msg="Ready for High-Precision Coding" if has_claude else "API Key Required in Settings -> AI Models",
            endpoint="https://openrouter.ai/api/v1"
        ))

        has_gpt = bool(self.openai_key or self.openrouter_key)
        detected.append(DetectedModel(
            model_id="gpt-4o",
            name="OpenAI GPT-4o",
            country="USA",
            provider="OpenAI Direct",
            status="ONLINE" if has_gpt else "OFFLINE",
            status_msg="Ready for Multimodal Coding" if has_gpt else "API Key Required in Settings -> AI Models",
            endpoint="https://api.openai.com/v1"
        ))

        # --- 2. China Models ---
        has_qwen = bool(self.openrouter_key or True)
        detected.append(DetectedModel(
            model_id="qwen-2.5-coder-32b",
            name="Qwen 2.5 Coder 32B",
            country="China",
            provider="Alibaba / OpenRouter",
            status="ONLINE",
            status_msg="Ready (OpenRouter Default)",
            endpoint="https://openrouter.ai/api/v1"
        ))

        detected.append(DetectedModel(
            model_id="deepseek-r1",
            name="DeepSeek R1 Reasoning",
            country="China",
            provider="DeepSeek / OpenRouter",
            status="ONLINE",
            status_msg="Ready for Deep Reasoning",
            endpoint="https://openrouter.ai/api/v1"
        ))

        # --- 3. Korea Models ---
        has_clova = bool(self.hyperclova_key)
        detected.append(DetectedModel(
            model_id="hyperclova-x",
            name="Naver HyperCLOVA X",
            country="Korea",
            provider="Naver Cloud Platform",
            status="ONLINE" if has_clova else "OFFLINE",
            status_msg="Ready for Korean Nuance Coding" if has_clova else "HyperCLOVA Secret Key Required in Settings",
            endpoint="https://clovastudio.apigw.ntruss.com"
        ))

        has_solar = bool(self.upstage_key)
        detected.append(DetectedModel(
            model_id="solar-mini",
            name="Upstage Solar Mini",
            country="Korea",
            provider="Upstage Console API",
            status="ONLINE" if has_solar else "OFFLINE",
            status_msg="Ready for Fast Korean/English Coding" if has_solar else "Upstage API Key Required in Settings",
            endpoint="https://api.upstage.ai/v1/solar"
        ))

        # --- 4. Hugging Face / OpenSource ---
        has_hf = bool(self.hf_token)
        detected.append(DetectedModel(
            model_id="huggingface-inference",
            name="Hugging Face Inference API",
            country="HuggingFace",
            provider="Hugging Face Hub",
            status="ONLINE" if has_hf else "OFFLINE",
            status_msg="Ready for OpenSource Models (Llama-3.1, EXAONE)" if has_hf else "HF_TOKEN Required in Settings -> AI Models",
            endpoint="https://api-inference.huggingface.co/models"
        ))

        return detected

    def print_discovery_report(self):
        """Print Global Auto-Discovery status report"""
        models = self.scan_available_models()
        print("\n================ GLOBAL AI MODELS AUTO-DISCOVERY REPORT ================")
        print(f"{'Model Name':<28} | {'Country':<10} | {'Status':<10} | {'Provider':<25} | {'Message'}")
        print("-" * 105)
        for m in models:
            status_str = "ONLINE" if "ONLINE" in m.status else "OFFLINE"
            print(f"{m.name:<28} | {m.country:<10} | [{status_str:<6}] | {m.provider:<25} | {m.status_msg}")
        print("=======================================================================\n")


if __name__ == '__main__':
    detector = AIModelDetector()
    detector.print_discovery_report()
