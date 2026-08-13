# -*- coding: utf-8 -*-
"""
Agent Smith - Model Configuration Schema & Pricing Directory
Supported LLM Provider & Model Cost Configurations
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelConfig:
    model_id: str
    name: str
    provider: str
    input_cost_per_m: float   # USD per 1,000,000 tokens
    output_cost_per_m: float  # USD per 1,000,000 tokens
    is_active: bool = True


# Pre-configured Enterprise Models Directory
DEFAULT_MODELS: Dict[str, ModelConfig] = {
    "claude-3-5-sonnet": ModelConfig(
        model_id="claude-3-5-sonnet",
        name="Anthropic Claude 3.5 Sonnet",
        provider="OpenRouter / Direct API",
        input_cost_per_m=3.00,
        output_cost_per_m=15.00
    ),
    "gpt-4o": ModelConfig(
        model_id="gpt-4o",
        name="OpenAI GPT-4o",
        provider="OpenAI Direct",
        input_cost_per_m=2.50,
        output_cost_per_m=10.00
    ),
    "qwen-2.5-coder-32b": ModelConfig(
        model_id="qwen-2.5-coder-32b",
        name="Qwen 2.5 Coder 32B",
        provider="OpenRouter",
        input_cost_per_m=0.30,
        output_cost_per_m=0.90
    ),
    "deepseek-r1": ModelConfig(
        model_id="deepseek-r1",
        name="DeepSeek R1 Reasoning",
        provider="OpenRouter",
        input_cost_per_m=0.55,
        output_cost_per_m=2.19
    ),
    "local-vllm-qwen": ModelConfig(
        model_id="local-vllm-qwen",
        name="On-Premise Red Hat vLLM Qwen",
        provider="On-Prem RHOAI (SNO)",
        input_cost_per_m=0.00,
        output_cost_per_m=0.00
    )
}
