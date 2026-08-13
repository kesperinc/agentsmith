# -*- coding: utf-8 -*-
"""
Agent Smith - Model Configuration Schema & Pricing Directory
Supported Global Models (USA, China, Korea, Hugging Face)
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelConfig:
    model_id: str
    name: str
    country: str              # "USA", "China", "Korea", "Global OS"
    provider: str
    input_cost_per_m: float   # USD per 1,000,000 tokens
    output_cost_per_m: float  # USD per 1,000,000 tokens
    is_active: bool = True


# Global Enterprise Models Directory (USA, China, Korea, Hugging Face)
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

    # --- China Models ---
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

    # --- Hugging Face / OpenSource ---
    "huggingface-inference": ModelConfig(
        model_id="huggingface-inference",
        name="Hugging Face Inference API",
        country="Global OS",
        provider="Hugging Face Hub (HF_TOKEN)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00
    ),
    "local-vllm-qwen": ModelConfig(
        model_id="local-vllm-qwen",
        name="On-Premise Red Hat vLLM Qwen",
        country="On-Premise",
        provider="On-Prem RHOAI (SNO)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00
    )
}
