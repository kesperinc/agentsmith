# -*- coding: utf-8 -*-
"""
Agent Smith - Model Configuration Schema & Pricing Directory
Supported Global Models (USA, China - including Kimi & GLM, Korea, HuggingFace, Local Engine)
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelConfig:
    model_id: str
    name: str
    country: str              # "USA", "China", "Korea", "HuggingFace", "Local"
    provider: str
    input_cost_per_m: float   # USD per 1,000,000 tokens
    output_cost_per_m: float  # USD per 1,000,000 tokens
    is_active: bool = True


# Global & Local Enterprise Models Directory
DEFAULT_MODELS: Dict[str, ModelConfig] = {
    # --- USA Models ---
    "claude-3-5-sonnet": ModelConfig(
        model_id="claude-3-5-sonnet",
        name="Anthropic Claude 3.5 Sonnet",
        country="USA",
        provider="Anthropic / OpenRouter",
        input_cost_per_m=3.00,
        output_cost_per_m=15.00
    ),
    "gpt-4o": ModelConfig(
        model_id="gpt-4o",
        name="OpenAI GPT-4o",
        country="USA",
        provider="OpenAI Direct",
        input_cost_per_m=2.50,
        output_cost_per_m=10.00
    ),
    "gemini-1.5-pro": ModelConfig(
        model_id="gemini-1.5-pro",
        name="Google Gemini 1.5 Pro",
        country="USA",
        provider="Google AI Studio",
        input_cost_per_m=1.25,
        output_cost_per_m=5.00
    ),

    # --- China Models (Qwen, DeepSeek, Kimi, GLM) ---
    "qwen-2.5-coder-32b": ModelConfig(
        model_id="qwen-2.5-coder-32b",
        name="Qwen 2.5 Coder 32B",
        country="China",
        provider="Alibaba / OpenRouter",
        input_cost_per_m=0.30,
        output_cost_per_m=0.90
    ),
    "deepseek-r1": ModelConfig(
        model_id="deepseek-r1",
        name="DeepSeek R1 Reasoning",
        country="China",
        provider="DeepSeek / OpenRouter",
        input_cost_per_m=0.55,
        output_cost_per_m=2.19
    ),
    "kimi-moonshot": ModelConfig(
        model_id="kimi-moonshot",
        name="Moonshot Kimi Chat 128k",
        country="China",
        provider="Moonshot AI Direct",
        input_cost_per_m=1.60,
        output_cost_per_m=4.80
    ),
    "glm-4": ModelConfig(
        model_id="glm-4",
        name="Zhipu GLM-4 / GLM-4 Flash",
        country="China",
        provider="Zhipu AI Direct",
        input_cost_per_m=0.10,
        output_cost_per_m=0.10
    ),

    # --- Korea Models ---
    "hyperclova-x": ModelConfig(
        model_id="hyperclova-x",
        name="Naver HyperCLOVA X",
        country="Korea",
        provider="Naver Cloud Platform",
        input_cost_per_m=2.00,
        output_cost_per_m=6.00
    ),
    "solar-mini": ModelConfig(
        model_id="solar-mini",
        name="Upstage Solar Mini",
        country="Korea",
        provider="Upstage Console API",
        input_cost_per_m=0.15,
        output_cost_per_m=0.15
    ),
    "exaone-3.0": ModelConfig(
        model_id="exaone-3.0",
        name="LG EXAONE 3.0 7.8B",
        country="Korea",
        provider="LG AI Research / Local",
        input_cost_per_m=0.20,
        output_cost_per_m=0.50
    ),

    # --- Hugging Face ---
    "huggingface-inference": ModelConfig(
        model_id="huggingface-inference",
        name="Hugging Face Inference API",
        country="HuggingFace",
        provider="Hugging Face Hub (HF_TOKEN)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00
    ),

    # --- Local Engines (Ollama, LM Studio, Custom vLLM) ---
    "local-ollama": ModelConfig(
        model_id="local-ollama",
        name="Local Ollama (localhost:11434)",
        country="Local",
        provider="Local GPU (Ollama Engine)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00
    ),
    "local-lmstudio": ModelConfig(
        model_id="local-lmstudio",
        name="Local LM Studio (localhost:1234)",
        country="Local",
        provider="Local GPU (LM Studio Engine)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00
    ),
    "local-vllm-qwen": ModelConfig(
        model_id="local-vllm-qwen",
        name="On-Premise Red Hat vLLM Qwen",
        country="Local",
        provider="On-Prem RHOAI (SNO)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00
    )
}
