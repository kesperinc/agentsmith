# -*- coding: utf-8 -*-
"""
Agent Smith - Global & Local AI Models Auto-Discovery & Health Detector Engine
Scans Environment API Keys (USA, China - Kimi/GLM, Korea, HuggingFace) & Local Endpoints (Ollama, LM Studio, vLLM)
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
    country: str       # "USA", "China", "Korea", "HuggingFace", "Local"
    provider: str
    status: str        # "ONLINE" or "OFFLINE"
    status_msg: str    # E.g., "Ready for Inference", "API Key Required"
    endpoint: str


class AIModelDetector:
    def __init__(self):
        # USA Keys
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")

        # China Keys (DeepSeek, Kimi, GLM)
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.moonshot_key = os.getenv("MOONSHOT_API_KEY", "") or os.getenv("KIMI_API_KEY", "")
        self.zhipu_key = os.getenv("ZHIPU_API_KEY", "") or os.getenv("GLM_API_KEY", "")

        # Korea Keys
        self.hyperclova_key = os.getenv("HYPERCLOVA_SECRET_KEY", "")
        self.upstage_key = os.getenv("UPSTAGE_API_KEY", "")

        # Hugging Face Key
        self.hf_token = os.getenv("HF_TOKEN", "")

        # Local Engine Endpoints
        self.ollama_url = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")
        self.lmstudio_url = os.getenv("LMSTUDIO_ENDPOINT", "http://localhost:1234/v1")
        self.local_vllm_url = os.getenv("VLLM_ENDPOINT", "http://localhost:8000/v1")

    def ping_endpoint(self, url: str) -> bool:
        """Generic endpoint HTTP ping check"""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AgentSmith/1.0"})
            with urllib.request.urlopen(req, timeout=1.2) as resp:
                return resp.status in (200, 204)
        except Exception:
            return False

    def scan_available_models(self) -> List[DetectedModel]:
        """Scan all models including China (Kimi, GLM) and Local Engines (Ollama, LM Studio)"""
        logging.info("Initiating Full Auto-Discovery scan (USA, China - Kimi/GLM, Korea, HuggingFace, Local)...")
        detected: List[DetectedModel] = []

        # --- 1. USA Models ---
        has_claude = bool(self.openrouter_key or self.anthropic_key)
        detected.append(DetectedModel(
            model_id="claude-3-5-sonnet",
            name="Anthropic Claude 3.5 Sonnet",
            country="USA",
            provider="Anthropic / OpenRouter",
            status="ONLINE" if has_claude else "OFFLINE",
            status_msg="Ready for High-Precision Coding" if has_claude else "API Key Required in Settings",
            endpoint="https://openrouter.ai/api/v1"
        ))

        has_gpt = bool(self.openai_key or self.openrouter_key)
        detected.append(DetectedModel(
            model_id="gpt-4o",
            name="OpenAI GPT-4o",
            country="USA",
            provider="OpenAI Direct",
            status="ONLINE" if has_gpt else "OFFLINE",
            status_msg="Ready for Multimodal Coding" if has_gpt else "API Key Required in Settings",
            endpoint="https://api.openai.com/v1"
        ))

        # --- 2. China Models (Qwen, DeepSeek, Kimi, GLM) ---
        detected.append(DetectedModel(
            model_id="qwen-2.5-coder-32b",
            name="Qwen 2.5 Coder 32B",
            country="China",
            provider="Alibaba / OpenRouter",
            status="ONLINE",
            status_msg="Ready (OpenRouter Default)",
            endpoint="https://openrouter.ai/api/v1"
        ))

        has_deepseek = bool(self.deepseek_key or self.openrouter_key)
        detected.append(DetectedModel(
            model_id="deepseek-r1",
            name="DeepSeek R1 Reasoning",
            country="China",
            provider="DeepSeek Direct / OpenRouter",
            status="ONLINE" if has_deepseek else "OFFLINE",
            status_msg="Ready for Deep Reasoning" if has_deepseek else "API Key Required in Settings",
            endpoint="https://api.deepseek.com/v1"
        ))

        has_kimi = bool(self.moonshot_key or self.openrouter_key)
        detected.append(DetectedModel(
            model_id="kimi-moonshot",
            name="Moonshot Kimi Chat 128k",
            country="China",
            provider="Moonshot AI Direct",
            status="ONLINE" if has_kimi else "OFFLINE",
            status_msg="Ready for Long-Context Coding" if has_kimi else "MOONSHOT_API_KEY Required in Settings",
            endpoint="https://api.moonshot.cn/v1"
        ))

        has_glm = bool(self.zhipu_key or self.openrouter_key)
        detected.append(DetectedModel(
            model_id="glm-4",
            name="Zhipu GLM-4 / GLM-4 Flash",
            country="China",
            provider="Zhipu AI Direct",
            status="ONLINE" if has_glm else "OFFLINE",
            status_msg="Ready for High-Speed Coding" if has_glm else "ZHIPU_API_KEY Required in Settings",
            endpoint="https://open.bigmodel.cn/api/paas/v4"
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
            status_msg="Ready for Fast Korean Coding" if has_solar else "Upstage API Key Required in Settings",
            endpoint="https://api.upstage.ai/v1/solar"
        ))

        # --- 4. Hugging Face ---
        has_hf = bool(self.hf_token)
        detected.append(DetectedModel(
            model_id="huggingface-inference",
            name="Hugging Face Inference API",
            country="HuggingFace",
            provider="Hugging Face Hub",
            status="ONLINE" if has_hf else "OFFLINE",
            status_msg="Ready for OpenSource Hub Models" if has_hf else "HF_TOKEN Required in Settings",
            endpoint="https://api-inference.huggingface.co/models"
        ))

        # --- 5. Local Engines (Ollama, LM Studio, Custom vLLM) ---
        ollama_online = self.ping_endpoint(f"{self.ollama_url}/api/tags")
        detected.append(DetectedModel(
            model_id="local-ollama",
            name="Local Ollama Engine",
            country="Local",
            provider="Local GPU (localhost:11434)",
            status="ONLINE" if ollama_online else "OFFLINE (Standby)",
            status_msg="Ollama Server Active & Models Loaded" if ollama_online else "Ollama Server Not Running (localhost:11434)",
            endpoint=self.ollama_url
        ))

        lmstudio_online = self.ping_endpoint(f"{self.lmstudio_url}/models")
        detected.append(DetectedModel(
            model_id="local-lmstudio",
            name="Local LM Studio Engine",
            country="Local",
            provider="Local GPU (localhost:1234)",
            status="ONLINE" if lmstudio_online else "OFFLINE (Standby)",
            status_msg="LM Studio Active & Ready" if lmstudio_online else "LM Studio Not Running (localhost:1234)",
            endpoint=self.lmstudio_url
        ))

        return detected

    def print_discovery_report(self):
        """Print Full Auto-Discovery status report"""
        models = self.scan_available_models()
        print("\n================ GLOBAL & LOCAL AI MODELS AUTO-DISCOVERY REPORT ================")
        print(f"{'Model Name':<28} | {'Country':<10} | {'Status':<10} | {'Provider':<25} | {'Message'}")
        print("-" * 105)
        for m in models:
            status_str = "ONLINE" if "ONLINE" in m.status else "OFFLINE"
            print(f"{m.name:<28} | {m.country:<10} | [{status_str:<6}] | {m.provider:<25} | {m.status_msg}")
        print("===============================================================================\n")


if __name__ == '__main__':
    detector = AIModelDetector()
    detector.print_discovery_report()
